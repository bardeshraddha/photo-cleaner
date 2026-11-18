"""Find pictures that probably came from chat apps (like WhatsApp) or social media.

How we tell:
  - Photos taken with a camera carry hidden "camera details": the phone model,
    the date the photo was taken, and so on. Chat apps remove these when they
    send a picture, and they make the picture smaller.
  - Some apps leave clues behind: their own naming pattern, a folder named after
    the app, or the app's name written inside the picture's hidden details.

Pictures are opened read-only. Nothing is changed.
"""

import os
import re

from PIL import Image

VERY_LIKELY = "very likely"
PROBABLY = "probably"

# Only these kinds of picture are checked. HEIC is the iPhone camera's own format
# (chat apps don't send it), and PNG files are mostly screenshots (Milestone 3).
CHECKED_EXTENSIONS = {".jpg", ".jpeg", ".webp"}

# WhatsApp shrinks pictures so the longest side is at most this many pixels.
# Phone and camera photos are usually much bigger (3,000 pixels or more).
CHAT_APP_MAX_SIDE = 1600

# Name patterns chat apps give to pictures, e.g. "IMG-20230101-WA0004.jpg".
CHAT_APP_NAMES = [
    (re.compile(r"^IMG-\d{8}-WA\d+", re.IGNORECASE), "WhatsApp"),
    (re.compile(r"^WhatsApp Image ", re.IGNORECASE), "WhatsApp"),
    (re.compile(r"^photo_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}"), "Telegram"),
    (re.compile(r"^signal-\d{4}-\d{2}-\d{2}"), "Signal"),
]

# Folder names that show where pictures came from, e.g. "WhatsApp Images".
CHAT_APP_FOLDERS = {"whatsapp": "WhatsApp", "telegram": "Telegram"}

# App names that can appear in a picture's hidden "made by" label.
APP_LABELS = {
    "instagram": "Instagram",
    "whatsapp": "WhatsApp",
    "facebook": "Facebook",
    "messenger": "Messenger",
    "snapchat": "Snapchat",
    "telegram": "Telegram",
}

# Numbers that pictures use to label their hidden details (a worldwide standard).
CAMERA_MAKE = 271        # e.g. "Apple"
CAMERA_MODEL = 272       # e.g. "iPhone 14 Pro"
MADE_BY = 305            # the app or software that saved the picture
CAMERA_SECTION = 0x8769  # the section holding the camera settings
DATE_TAKEN = 36867       # when the photo was taken


def read_details(path):
    """Read a picture's size and hidden camera details. Returns None if it can't be read.

    The file is opened read-only ("rb"). Pillow only reads the start of the file,
    where these details are kept, so this is quick even for big pictures.
    """
    try:
        with open(path, "rb") as f:
            image = Image.open(f)
            details = image.getexif()
            camera = details.get_ifd(CAMERA_SECTION)
            return {
                "width": image.width,
                "height": image.height,
                "camera_make": details.get(CAMERA_MAKE),
                "camera_model": details.get(CAMERA_MODEL),
                "date_taken": camera.get(DATE_TAKEN),
                "made_by": details.get(MADE_BY),
            }
    except Exception:
        # A damaged or unusual file: skip it quietly rather than show a scary error.
        return None


def judge(name, folders, details):
    """Decide whether a picture came from a chat app or social media.

    Returns (level, reason), where the reason is in plain words,
    or None if the picture looks like the person's own photo.
    This part has no Mac-specific code, so the same rules can move to a phone app.
    """
    for pattern, app in CHAT_APP_NAMES:
        if pattern.search(name):
            return VERY_LIKELY, f"the name looks like a {app} picture"

    for folder in folders:
        for word, app in CHAT_APP_FOLDERS.items():
            if word in folder.lower():
                return VERY_LIKELY, f"it is in a {app} folder"

    made_by = str(details.get("made_by") or "").lower()
    for word, app in APP_LABELS.items():
        if word in made_by:
            return VERY_LIKELY, f"it was saved by {app}"

    has_camera_details = any(
        details.get(key) for key in ("camera_make", "camera_model", "date_taken")
    )
    longest_side = max(details["width"], details["height"])
    if not has_camera_details and longest_side <= CHAT_APP_MAX_SIDE:
        return PROBABLY, "it has no camera details and is the small size chat apps send"

    return None


def find_forwarded(folder, paths):
    """Check each picture. Returns a list of (path, level, reason).

    "Very likely" pictures come first, then the biggest first.
    Pictures that can't be read are skipped.
    """
    results = []
    for path in paths:
        if os.path.splitext(path)[1].lower() not in CHECKED_EXTENSIONS:
            continue
        details = read_details(path)
        if details is None:
            continue
        # Only look at folder names inside the folder being checked.
        folders = os.path.relpath(path, folder).split(os.sep)[:-1]
        verdict = judge(os.path.basename(path), folders, details)
        if verdict:
            level, reason = verdict
            results.append((path, level, reason))

    results.sort(key=lambda r: (r[1] != VERY_LIKELY, -os.path.getsize(r[0]), r[0]))
    return results
