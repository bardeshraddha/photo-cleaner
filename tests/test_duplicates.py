"""Automatic checks for finding duplicates. Run with:  python3 -m unittest discover tests"""

import os
import tempfile
import unittest

from photo_cleaner.duplicates import extra_space, find_duplicates
from photo_cleaner.report import build_report
from photo_cleaner.scan import find_photos


class FindDuplicatesTest(unittest.TestCase):

    def setUp(self):
        # Each test gets a brand-new practice folder, thrown away automatically afterwards.
        practice = tempfile.TemporaryDirectory()
        self.addCleanup(practice.cleanup)
        self.folder = practice.name

    def make_file(self, relative_path, contents):
        """Create a small fake photo inside the practice folder and return its path."""
        path = os.path.join(self.folder, relative_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(contents)
        return path

    def snapshot(self):
        """Every file in the practice folder, with its contents and last-changed time."""
        result = {}
        for current_folder, _, names in os.walk(self.folder):
            for name in names:
                path = os.path.join(current_folder, name)
                with open(path, "rb") as f:
                    result[path] = (f.read(), os.path.getmtime(path))
        return result

    def test_identical_photos_are_found(self):
        original = self.make_file("2023/IMG_0012.jpg", b"beach photo")
        copy = self.make_file("WhatsApp/IMG-20230101-WA0004.jpg", b"beach photo")
        self.make_file("2023/IMG_0013.jpg", b"a different photo")

        groups = find_duplicates(find_photos(self.folder))

        self.assertEqual(len(groups), 1)
        self.assertEqual(set(groups[0]), {original, copy})

    def test_same_size_but_different_contents_is_not_a_duplicate(self):
        self.make_file("a.jpg", b"photo A")
        self.make_file("b.jpg", b"photo B")

        self.assertEqual(find_duplicates(find_photos(self.folder)), [])

    def test_space_to_free_is_added_up_correctly(self):
        for name in ["big.jpg", "big copy.jpg", "big copy 2.jpg"]:
            self.make_file(name, b"x" * 1000)
        for name in ["small.jpg", "small copy.jpg"]:
            self.make_file(name, b"y" * 500)

        groups = find_duplicates(find_photos(self.folder))

        self.assertEqual(sum(extra_space(group) for group in groups), 2500)
        report = build_report(self.folder, 5, groups)
        self.assertIn("You could free up about 2.5 KB", report)

    def test_oldest_copy_is_suggested_to_keep(self):
        self.make_file("Album/IMG_0012.jpg", b"birthday photo")
        older = self.make_file("Phone/IMG_0012.jpg", b"birthday photo")
        september_2020 = 1_600_000_000  # computers count time in seconds since 1970
        os.utime(older, (september_2020, september_2020))

        groups = find_duplicates(find_photos(self.folder))

        self.assertEqual(groups[0][0], older)

    def test_scan_does_not_change_any_file(self):
        self.make_file("a.jpg", b"same photo")
        self.make_file("copy of a.jpg", b"same photo")
        self.make_file("notes.txt", b"not a photo")
        before = self.snapshot()

        groups = find_duplicates(find_photos(self.folder))
        build_report(self.folder, 2, groups)

        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
