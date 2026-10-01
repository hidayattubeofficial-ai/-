# Hidayat Video Command Library — /goldenhour Resolution

## Decision
Canonical ownership of `/goldenhour` is **v1 Weather, Lighting & Effects**.

## Reason
`/goldenhour` is already present in the verified v1 command set. The identical command name in v2 Time & Atmosphere is therefore treated as a cross-version duplicate, not a second canonical command.

## Registry accounting
- v1 canonical commands: 98
- v2 listed additions: 75
- v1+v2 unique command names: **172**
- v3 canonical-expansion candidates: 49
- Combined current unique command names: **221**

## Preservation rule
The existing v2 lock/index is preserved unchanged for historical integrity. The v2 `/goldenhour` entry remains in its source batch as a documented duplicate, but must not be emitted twice in any future canonical machine-readable registry.

## Final-lock requirement
Future aggregate exports must deduplicate by exact command name and retain the v1 `/goldenhour` definition as the canonical record.

## Status
**Resolution recorded. Full-library validation may proceed.**
