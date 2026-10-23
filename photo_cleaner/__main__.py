"""The starting point. Run with:  python3 -m photo_cleaner "/path/to/photo folder" """

import os
import sys

from .duplicates import find_duplicates
from .report import build_report
from .scan import find_photos


def main(args):
    """Check one folder and print the report. Returns 0 if all went well, 1 if not."""
    if len(args) != 1:
        print("Please tell me which folder to check, like this:")
        print('  python3 -m photo_cleaner "/path/to/photo folder"')
        return 1

    folder = os.path.expanduser(args[0])
    if not os.path.isdir(folder):
        print(f'I couldn\'t find a folder called "{args[0]}".')
        print("Please check the spelling. Tip: you can drag the folder into this window")
        print("to fill in its location for you.")
        return 1

    print("Checking your photos. Large folders can take a few minutes...")
    try:
        photos = find_photos(folder)
        groups = find_duplicates(photos)
    except KeyboardInterrupt:
        print("\nStopped. Nothing has been changed.")
        return 1

    print()
    print(build_report(folder, len(photos), groups))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
