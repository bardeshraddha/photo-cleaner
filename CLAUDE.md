# Photo Cleaner

## Goal

A Python tool that looks through a folder of photos and lists clutter that wastes phone storage,
for **elderly users** who want to free up space:

1. **Exact duplicates:** the same photo saved more than once. (Milestone 1)
2. **Forwarded images:** pictures that came in through chat apps such as WhatsApp. (Milestone 2)
3. **Text-heavy photos:** screenshots, photos of documents, memes covered in text. (Milestone 3)

Output must be calm, plain and easy to read: sizes in MB/GB, no jargon, no scary errors.

## Where this is heading

This Python tool is a **Mac prototype** to prove the detection works. The real goal is a
**phone app for elderly users** that processes photos **on the phone**, so they never leave it.

- Prefer detection methods that could also run on a phone (no internet services, no uploads).
- Keep the detection logic separate from the Mac-specific parts, so it's easy to port later.

## The most important rule: NEVER delete files

- The tool **only lists** files and says how much space could be freed. The person decides what to do.
- Code must open files **read-only**. Never use `os.remove`, `os.unlink`, `shutil.rmtree`,
  `os.rename`, `shutil.move`, or anything else that deletes, moves, renames or changes a file.
- Every report ends by reminding the reader that nothing was deleted.
- Tests must check that every file is still there, unchanged, after a scan.

## How to work on this project

- This project is built step by step for a **non-technical reader**: explain every step in
  plain, simple English. Avoid jargon, or explain it when it's needed.
- **Before creating or changing any file:** show the full contents in the chat, explain what
  the file is for, and wait for a "go".

## Decision log

- Important decisions are recorded in `docs/decisions.md`.
- When we make a new decision (a new approach, a trade-off, or a change of direction), suggest
  an entry and show it before adding it. Add new entries at the bottom, numbered in order.
- Each entry uses: **Date**, **Decision**, **Why**, **Alternatives considered**, **Revisit when**.
- Read the log before planning a new milestone, and point out any "Revisit when" that now applies.

## How to run

```
python3 -m photo_cleaner "/path/to/photo folder"   # run the tool
python3 -m unittest discover tests                  # run the automatic checks
```

- Built-in macOS Python 3.9.6. Milestone 1 uses only Python's standard library (nothing to install).
- Later milestones need Pillow (Milestone 2) and Tesseract OCR (Milestone 3).

## Project structure

```
photo_cleaner/
  __main__.py     starting point (reads the folder path, prints the report)
  scan.py         finds photo files in a folder
  duplicates.py   finds exact duplicates (group by size, then SHA-256 fingerprint)
  report.py       prints friendly results
tests/            automatic checks (unittest)
docs/             project notes, including the decision log
```
