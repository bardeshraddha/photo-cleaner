"""Turn the results into a friendly, easy-to-read message."""

import os

from .duplicates import extra_space

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


def build_report(folder, photo_count, groups):
    """Return the whole report as text, ready to print."""
    folder = os.path.abspath(folder)
    name = os.path.basename(folder) or folder
    parent = os.path.dirname(folder)

    def show(path):
        # Show paths starting from the folder's name, e.g. "Phone Backup/2023/IMG_0012.jpg".
        return os.path.relpath(os.path.abspath(path), parent)

    lines = [f'Photo Cleaner: checked {plural(photo_count, "photo")} in "{name}"', ""]

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

        total = sum(extra_space(group) for group in groups)
        lines.append("")
        lines.append(f"You could free up about {human_size(total)} by removing the extra copies.")

    lines.append("Nothing has been deleted. This is only a list.")
    return "\n".join(lines)
