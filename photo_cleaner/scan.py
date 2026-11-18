"""Find all the photo files inside a folder."""

import os

# File endings we treat as photos. We compare in lower case, so ".JPG" counts too.
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".gif", ".webp"}

# The Mac Photos app keeps its library in a special folder that looks like one file
# in Finder. Inside are thousands of the app's own small preview copies, which
# aren't real photos, and the Photos app manages them itself. So we skip it.
APP_LIBRARY_ENDINGS = (".photoslibrary",)


def find_photos(folder):
    """Return a sorted list of paths to every photo in `folder` and the folders inside it.

    Hidden files and folders (names starting with ".") are skipped, and so are
    shortcuts (links) to other files and Photos app libraries. Nothing is opened
    or changed here; we only look at file names.
    """
    photos = []
    for current_folder, subfolders, filenames in os.walk(folder):
        # Don't go into hidden folders such as ".Trash", or into Photos app libraries.
        subfolders[:] = [
            name for name in subfolders
            if not name.startswith(".") and not name.lower().endswith(APP_LIBRARY_ENDINGS)
        ]
        for name in filenames:
            if name.startswith("."):
                continue
            path = os.path.join(current_folder, name)
            # A shortcut takes up no real space, so it isn't a duplicate worth listing.
            if os.path.islink(path):
                continue
            extension = os.path.splitext(name)[1].lower()
            if extension in PHOTO_EXTENSIONS:
                photos.append(path)
    return sorted(photos)
