"""Find photos that are exact copies of each other."""

import hashlib
import os
from collections import defaultdict

# Read files 1 MB at a time, so even very large files don't fill up the computer's memory.
CHUNK_SIZE = 1024 * 1024


def fingerprint(path):
    """Return a short code (a SHA-256 hash) that is the same only for identical files.

    The file is opened read-only ("rb" = read, binary), so it cannot be changed.
    """
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(paths):
    """Group files with identical contents.

    Returns a list of groups. Each group is a list of two or more identical files,
    oldest first (the oldest is most likely the original). The groups that would
    free up the most space come first. Files that can't be read are skipped.
    """
    # Round 1: files of different sizes can't be identical, so group by size first.
    by_size = defaultdict(list)
    for path in paths:
        try:
            by_size[os.path.getsize(path)].append(path)
        except OSError:
            continue

    # Round 2: only fingerprint files that share a size with another file.
    groups = []
    for same_size in by_size.values():
        if len(same_size) < 2:
            continue
        by_fingerprint = defaultdict(list)
        for path in same_size:
            try:
                by_fingerprint[fingerprint(path)].append(path)
            except OSError:
                continue
        for group in by_fingerprint.values():
            if len(group) > 1:
                groups.append(sorted(group, key=lambda p: (os.path.getmtime(p), p)))

    groups.sort(key=lambda group: (-extra_space(group), group[0]))
    return groups


def extra_space(group):
    """How many bytes would be freed by removing every copy except the first."""
    return os.path.getsize(group[0]) * (len(group) - 1)
