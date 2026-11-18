"""Automatic checks for finding pictures from chat apps. Run with:  python3 -m unittest discover tests"""

import os
import tempfile
import unittest

from PIL import Image

from photo_cleaner.duplicates import find_duplicates
from photo_cleaner.forwarded import PROBABLY, VERY_LIKELY, find_forwarded
from photo_cleaner.report import build_report, human_size
from photo_cleaner.scan import find_photos


class FindForwardedTest(unittest.TestCase):

    def setUp(self):
        # Each test gets a brand-new practice folder, thrown away automatically afterwards.
        practice = tempfile.TemporaryDirectory()
        self.addCleanup(practice.cleanup)
        self.folder = practice.name

    def make_picture(self, relative_path, size, camera=None, made_by=None):
        """Create a small practice picture, optionally with camera details or an app label."""
        path = os.path.join(self.folder, relative_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        details = Image.Exif()
        if camera:
            details[271] = "Apple"   # camera make
            details[272] = camera    # camera model
        if made_by:
            details[305] = made_by   # the app that saved it
        Image.new("RGB", size, "skyblue").save(path, exif=details)
        return path

    def check(self, folder=None):
        """Run the chat-app check, returning {file name: (level, reason)}."""
        folder = folder or self.folder
        results = find_forwarded(folder, find_photos(folder))
        return {os.path.basename(path): (level, reason) for path, level, reason in results}

    def snapshot(self):
        """Every file in the practice folder, with its contents and last-changed time."""
        result = {}
        for current_folder, _, names in os.walk(self.folder):
            for name in names:
                path = os.path.join(current_folder, name)
                with open(path, "rb") as f:
                    result[path] = (f.read(), os.path.getmtime(path))
        return result

    def test_small_picture_without_camera_details_is_probably_from_a_chat_app(self):
        # Like "Image - family.jpg": a family photo sent through WhatsApp.
        self.make_picture("Image - family.jpg", (768, 1024), made_by="Picasa")

        self.assertEqual(self.check()["Image - family.jpg"][0], PROBABLY)

    def test_instagram_label_is_very_likely(self):
        # Like the real picture saved from Instagram.
        self.make_picture("0E02ABC5.jpg", (828, 1472), made_by="Instagram")

        level, reason = self.check()["0E02ABC5.jpg"]
        self.assertEqual(level, VERY_LIKELY)
        self.assertIn("Instagram", reason)

    def test_chat_app_names_are_very_likely(self):
        for name in ["IMG-20230101-WA0004.jpg", "WhatsApp Image 2023-01-01 at 10.15.32.jpeg",
                     "photo_2023-01-01_10-15-32.jpg", "signal-2023-01-01-101532.jpg"]:
            # Even with camera details, the name gives it away.
            self.make_picture(name, (1200, 1600), camera="iPhone 14 Pro")

        results = self.check()

        self.assertEqual(len(results), 4)
        self.assertTrue(all(level == VERY_LIKELY for level, _ in results.values()))

    def test_picture_in_a_whatsapp_folder_is_very_likely(self):
        self.make_picture("WhatsApp Images/holiday.jpg", (3024, 4032), camera="iPhone 14 Pro")

        self.assertEqual(self.check()["holiday.jpg"][0], VERY_LIKELY)

    def test_only_folders_inside_the_checked_folder_count(self):
        # Checking a folder that is itself called "WhatsApp backup" shouldn't flag everything in it.
        self.make_picture("WhatsApp backup/my photo.jpg", (3024, 4032), camera="iPhone 14 Pro")

        self.assertEqual(self.check(os.path.join(self.folder, "WhatsApp backup")), {})

    def test_own_camera_photo_is_not_listed(self):
        # Like IMG_2374.jpg. Even a small photo is left alone if it has camera details.
        self.make_picture("IMG_2374.jpg", (3024, 4032), camera="iPhone 14 Pro")
        self.make_picture("IMG_2375.jpg", (800, 600), camera="iPhone 14 Pro")

        self.assertEqual(self.check(), {})

    def test_big_picture_without_camera_details_is_not_listed(self):
        # Like the Maui photos: no camera details, but far too big to come from a chat app.
        self.make_picture("shraddha 1.jpg", (2389, 3583))

        self.assertEqual(self.check(), {})

    def test_png_and_heic_are_skipped(self):
        # PNGs are mostly screenshots (Milestone 3); HEIC is the iPhone camera's own format.
        self.make_picture("screenshot.png", (828, 1472))
        with open(os.path.join(self.folder, "camera.heic"), "wb") as f:
            f.write(b"pretend iPhone photo")

        self.assertEqual(self.check(), {})

    def test_damaged_picture_is_skipped_quietly(self):
        with open(os.path.join(self.folder, "broken.jpg"), "wb") as f:
            f.write(b"this is not really a picture")

        self.assertEqual(self.check(), {})

    def test_very_likely_pictures_come_first(self):
        self.make_picture("small family.jpg", (768, 1024))
        self.make_picture("IMG-20230101-WA0004.jpg", (640, 480))

        names = list(self.check())

        self.assertEqual(names, ["IMG-20230101-WA0004.jpg", "small family.jpg"])

    def test_photos_library_inside_the_folder_is_skipped(self):
        # The Mac Photos app keeps thousands of small preview copies inside its library.
        # They aren't real photos, so they must not be listed.
        self.make_picture("Photos Library.photoslibrary/resources/preview.jpg", (360, 480))
        self.make_picture("Image - family.jpg", (768, 1024))

        self.assertEqual(list(self.check()), ["Image - family.jpg"])

    def test_report_has_gentle_warning_and_counts_each_picture_once(self):
        # A family photo from WhatsApp, saved twice: it's in BOTH lists.
        family = self.make_picture("Image - family.jpg", (768, 1024))
        self.make_picture("Image - family copy.jpg", (768, 1024))
        photos = find_photos(self.folder)

        report = build_report(self.folder, len(photos), find_duplicates(photos),
                              find_forwarded(self.folder, photos))

        self.assertIn("Some may be precious family photos", report)
        # Two pictures in total, so the most that could be freed is two pictures' worth, not three.
        self.assertIn(f"Altogether, you could free up about {human_size(2 * os.path.getsize(family))}", report)
        self.assertTrue(report.endswith("Nothing has been deleted. This is only a list."))

    def test_check_does_not_change_any_file(self):
        self.make_picture("Image - family.jpg", (768, 1024))
        self.make_picture("IMG_2374.jpg", (3024, 4032), camera="iPhone 14 Pro")
        self.make_picture("WhatsApp Images/greeting.jpg", (800, 800))
        before = self.snapshot()

        self.check()

        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
