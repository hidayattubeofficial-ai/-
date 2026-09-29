#!/usr/bin/env python3
"""Portable, read-only local verification gate.

Runs before GitHub PR creation. It never uploads, publishes, deploys, or pushes.
Standard-library only so the verifier itself has minimal dependency risk.
"""
from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

REPO_MARKERS = (".git", "PROJECT_NOTEBOOK.md", "LOCAL_VERIFICATION_ENGINE.md")
IGNORED_BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".mp3",
    ".wav", ".woff", ".woff2", ".ttf", ".otf", ".lock",
}
SECRET_PATTERNS = [
    re.compile(r"""(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['"][^'"]{12,}['"]"""),
    re.compile(r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
FORBIDDEN_EXECUTION = (
    "upload_private_youtube.py",
    "youtube.videos().insert",
    "wrangler deploy",
    "cloudflare/pages-action",
)


def run(cmd, cwd, timeout=300):
    try:
        p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    except FileNotFoundError:
        return False, f"missing tool: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout}s: {' '.join(cmd)}"
    return p.returncode == 0, (p.stdout + "\n" + p.stderr).strip()[-6000:]


def find_root(start):
    for p in (start, *start.parents):
        if (p / ".git").exists() or all((p / m).exists() for m in REPO_MARKERS[1:]):
            return p
    raise RuntimeError("repository root not found; run from a checked-out repository")


def git_paths(root, command):
    ok, out = run(command, root)
    if not ok:
        raise RuntimeError(out)
    return {root / x for x in out.splitlines() if x}


def verification_files(root):
    """Return tracked + non-ignored untracked files that exist on disk."""
    tracked = git_paths(root, ["git", "ls-files"])
    untracked = git_paths(root, ["git", "ls-files", "--others", "--exclude-standard"])
    return sorted(
        {p for p in tracked | untracked if p.is_file()},
        key=lambda p: str(p),
    )


def changed_files(root):
    """Include staged/unstaged tracked changes and non-ignored untracked files."""
    changed = git_paths(root, ["git", "diff", "--name-only", "HEAD"])
    untracked = git_paths(root, ["git", "ls-files", "--others", "--exclude-standard"])
    return sorted(
        {p for p in changed | untracked if p.is_file()},
        key=lambda p: str(p),
    )


def python_check(root, files):
    errors = []
    for path in [p for p in files if p.suffix == ".py"]:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError, UnicodeError) as e:
            errors.append(f"{path.relative_to(root)}: {e}")
    return not errors, ("Python AST: OK" if not errors else "\n".join(errors))


def secret_check(root, files):
    hits = []
    for path in files:
        if path.suffix.lower() in IGNORED_BINARY_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            hits.append(str(path.relative_to(root)))
    return not hits, (
        "Secrets scan: OK"
        if not hits
        else "possible secret in: " + ", ".join(hits)
    )


def policy_check(root, files):
    violations = []
    for path in files:
        if ".github/workflows/" not in path.as_posix() or path.suffix not in {".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in FORBIDDEN_EXECUTION:
            if marker in text:
                violations.append(
                    f"{path.relative_to(root)} contains forbidden production execution: {marker}"
                )
    return not violations, ("Policy gate: OK" if not violations else "\n".join(violations))


def test_check(root):
    if not any((root / p).is_dir() for p in ("tests", "test")):
        return True, "Tests: no repository test suite detected"
    if not any((root / p).exists() for p in ("pytest.ini", "pyproject.toml", "setup.cfg")):
        return True, "Tests: suite/config not declared; static checks continue"
    return run([sys.executable, "-m", "pytest", "-q"], root, 600)


def build_check(root):
    if (root / "package.json").exists():
        return run(["npm", "run", "build"], root, 600)
    if (root / "gradlew").exists():
        return run(["./gradlew", "assembleDebug"], root, 900)
    return True, "Build: no declared package/Gradle entrypoint detected; skipped safely"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--changed-only",
        action="store_true",
        help="scan staged/unstaged changes plus non-ignored untracked files",
    )
    ap.add_argument("--security-only", action="store_true")
    ap.add_argument("--build", action="store_true")
    args = ap.parse_args()

    try:
        root = find_root(Path.cwd().resolve())
        files = changed_files(root) if args.changed_only else verification_files(root)
    except Exception as e:
        print("RED  repository discovery:", e)
        return 2

    if not files:
        print("RED  verification scope is empty; refusing to report GREEN.")
        return 2

    results = [
        ("Python syntax", *python_check(root, files)),
        ("Secret scan", *secret_check(root, files)),
        ("Policy gate", *policy_check(root, files)),
    ]
    if not args.security_only:
        results.append(("Tests", *test_check(root)))
        if args.build:
            results.append(("Build", *build_check(root)))

    print(f"\nLocal Verification Engine — {root}\n" + "=" * 72)
    for name, ok, detail in results:
        print(f"{'GREEN' if ok else 'RED  '} {name}\n      {detail}")
    print("=" * 72)

    failed = [name for name, ok, _ in results if not ok]
    if failed:
        print("RED  verification failed; do not create/push a PR.")
        return 1

    print("GREEN local verification passed.")
    print("SAFE  no YouTube upload, Cloudflare deploy, or git push is performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
