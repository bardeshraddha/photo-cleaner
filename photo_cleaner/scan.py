"""Find all the photo files inside a folder."""

import os

# File endings we treat as photos. We compare in lower case, so ".JPG" counts too.
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".gif", ".webp"}


def find_photos(folder):
    """Return a sorted list of paths to every photo in `folder` and the folders inside it.

    Hidden files and folders (names starting with ".") are skipped, and so are
    shortcuts (links) to other files. Nothing is opened or changed here; we only
    look at file names.
    """
    photos = []
    for current_folder, subfolders, filenames in os.walk(folder):
        # Don't go into hidden folders such as ".Trash".
        subfolders[:] = [name for name in subfolders if not name.startswith(".")]
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
