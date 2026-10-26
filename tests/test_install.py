import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("library_install", Path(__file__).resolve().parents[1] / "tools/install.py")
INSTALL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALL)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.destination = self.root / "installed"
        self.names = ["reconstruct-orchestrate", "reconstruct-verify"]
        for name in self.names:
            directory = self.source / name
            directory.mkdir(parents=True)
            (directory / "SKILL.md").write_text(name)
        references = self.source / "reconstruct-orchestrate/references"
        references.mkdir()
        (references / "skill-map.json").write_text(json.dumps({"skills": [{"name": n} for n in self.names]}))

    def test_dry_run_has_no_filesystem_side_effect(self):
        self.assertEqual(INSTALL.install(self.source, self.destination, True), self.names)
        self.assertFalse(self.destination.exists())

    def test_complete_copy_and_reinstallation_refusal(self):
        INSTALL.install(self.source, self.destination)
        for name in self.names:
            self.assertEqual((self.destination / name / "SKILL.md").read_text(), name)
        with self.assertRaises(FileExistsError):
            INSTALL.install(self.source, self.destination)

    @unittest.skipUnless(os.name == "posix", "POSIX file modes only")
    def test_world_writable_source_modes_are_not_propagated(self):
        (self.source / self.names[0]).chmod(0o777)
        (self.source / self.names[0] / "SKILL.md").chmod(0o777)
        INSTALL.install(self.source, self.destination)
        for name in self.names:
            for path in (self.destination / name, self.destination / name / "SKILL.md"):
                self.assertEqual(path.stat().st_mode & 0o022, 0)

    def test_collision_preflight_leaves_other_skills_untouched(self):
        existing = self.destination / self.names[1]
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("user content")
        with self.assertRaises(FileExistsError):
            INSTALL.install(self.source, self.destination)
        self.assertEqual((existing / "SKILL.md").read_text(), "user content")
        self.assertFalse((self.destination / self.names[0]).exists())

    def test_missing_skill_does_not_partially_install(self):
        (self.source / self.names[1] / "SKILL.md").unlink()
        with self.assertRaises(ValueError):
            INSTALL.install(self.source, self.destination)
        self.assertFalse(self.destination.exists())

    def test_dangling_symlink_is_also_a_collision(self):
        self.destination.mkdir()
        (self.destination / self.names[1]).symlink_to(self.root / "absent")
        with self.assertRaises(FileExistsError):
            INSTALL.install(self.source, self.destination)

    def test_destination_inside_source_is_rejected_before_recursive_copy(self):
        destination = self.source / self.names[0] / "nested-install"
        with self.assertRaisesRegex(ValueError, "inside source skill"):
            INSTALL.install(self.source, destination)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
