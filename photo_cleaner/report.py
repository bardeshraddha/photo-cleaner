"""Turn the results into a friendly, easy-to-read message."""

import os

from .duplicates import extra_space
from .forwarded import PROBABLY, VERY_LIKELY

# Lines in a group start after this much space, so the file names line up neatly.
INDENT = " " * 17


def human_size(num_bytes):
    """Show a size the way phones and Macs do, e.g. "2.1 MB" or "1.4 GB"."""
    if num_bytes >= 1000 ** 3:
        return f"{num_bytes / 1000 ** 3:.1f} GB"
    if num_bytes >= 1000 ** 2:
        return f"{num_bytes / 1000 ** 2:.1f} MB"
    return f"{num_bytes / 1000:.1f} KB"


def plural(count, word):
    """Return e.g. "1 photo" or "3 photos"."""
    return f"{count:,} {word}" + ("" if count == 1 else "s")


def build_report(folder, photo_count, groups, forwarded=()):
    """Return the whole report as text, ready to print.

    `groups` are the identical photos (from duplicates.py).
    `forwarded` are the pictures from chat apps (from forwarded.py).
    """
    folder = os.path.abspath(folder)
    name = os.path.basename(folder) or folder
    parent = os.path.dirname(folder)

    def show(path):
        # Show paths starting from the folder's name, e.g. "Phone Backup/2023/IMG_0012.jpg".
        return os.path.relpath(os.path.abspath(path), parent)

    lines = [f'Photo Cleaner: checked {plural(photo_count, "photo")} in "{name}"']

    # Part 1: identical photos.
    lines += ["", "1. Identical photos", ""]
    if not groups:
        lines.append("Good news: no identical photos were found.")
    else:
        lines.append(f"Found {plural(len(groups), 'group')} of identical photos.")
        for number, group in enumerate(groups, start=1):
            size = human_size(os.path.getsize(group[0]))
            lines.append("")
            lines.append(f"Group {number}: {len(group)} identical copies ({size} each)")
            lines.append(f"  Keep:          {show(group[0])}")
            lines.append(f"  Extra copies:  {show(group[1])}")
            for path in group[2:]:
                lines.append(INDENT + show(path))
        duplicates_total = sum(extra_space(group) for group in groups)
        lines.append("")
        lines.append(
            f"You could free up about {human_size(duplicates_total)} by removing the extra copies."
        )

    # Part 2: pictures from chat apps and social media.
    lines += ["", "2. Pictures from chat apps and social media", ""]
    if not forwarded:
        lines.append("Good news: no pictures from chat apps or social media were found.")
    else:
        lines.append("These were probably sent to you by other people, or saved from apps")
        lines.append("like WhatsApp or Instagram. Some may be precious family photos,")
        lines.append("so please look through them before removing any.")
        sections = [
            (VERY_LIKELY, "Very likely from a chat app or social media"),
            (PROBABLY, "Probably from a chat app (no camera details, and the small size chat apps send)"),
        ]
        for level, title in sections:
            items = [(path, reason) for path, item_level, reason in forwarded if item_level == level]
            if not items:
                continue
            size = sum(os.path.getsize(path) for path, _ in items)
            lines.append("")
            lines.append(f"{title}: {plural(len(items), 'picture')}, {human_size(size)}")
            for path, reason in items:
                line = f"  {human_size(os.path.getsize(path)):>9}  {show(path)}"
                if level == VERY_LIKELY:
                    line += f"  ({reason})"
                lines.append(line)

    # The grand total. A picture can be in both lists, so we count each one only once.
    if groups and forwarded:
        extra_copies = {path for group in groups for path in group[1:]}
        forwarded_total = sum(
            os.path.getsize(path) for path, _, _ in forwarded if path not in extra_copies
        )
        grand_total = sum(extra_space(group) for group in groups) + forwarded_total
        lines.append("")
        lines.append(f"Altogether, you could free up about {human_size(grand_total)}.")
        lines.append("(Pictures that appear in both lists are only counted once.)")

    lines += ["", "Nothing has been deleted. This is only a list."]
    return "\n".join(lines)
