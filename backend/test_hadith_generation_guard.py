from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hadith_generation_guard import prepare_generation
from hadith_identity import make_identity
from hadith_revision_registry import next_revision


class HadithGenerationGuardTests(unittest.TestCase):
    def test_new_hadith_gets_canonical_slot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = prepare_generation(tmp, "sahih-bukhari", 2)
            self.assertEqual(result.request.identity.sequence_key, "sahih-bukhari/2")
            self.assertEqual(
                result.output_path,
                Path(tmp) / "sahih-bukhari" / "2",
            )

    def test_existing_canonical_hadith_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sahih-bukhari" / "2"
            target.mkdir(parents=True)

            with self.assertRaises(FileExistsError):
                prepare_generation(tmp, "sahih-bukhari", 2)

    def test_edit_requires_explicit_request_and_creates_next_revision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            identity = make_identity("sahih-bukhari", 2)
            v1 = Path(tmp) / identity.book / "2" / "v1"
            v1.mkdir(parents=True)

            result = prepare_generation(
                tmp,
                "sahih-bukhari",
                2,
                action="edit",
                explicit_request=True,
                existing_revisions=[1],
            )
            self.assertEqual(result.revision.revision, 2)
            self.assertTrue(result.output_path.exists())

    def test_next_revision_ignores_invalid_values(self) -> None:
        self.assertEqual(next_revision([0, -1, 1, 3]), 4)


if __name__ == "__main__":
    unittest.main()
