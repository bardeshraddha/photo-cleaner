# Photo Cleaner

Photo Cleaner looks through a folder of photos and tells you which ones are
**exact copies** of each other, and how much space you could free up by
removing the extra copies.

**Photo Cleaner never deletes anything.** It only gives you a list.
You decide what to keep and what to remove.

## What you need

- A Mac. It uses the Python that comes built in, so there is nothing to install.

## How to use it

1. Open the **Terminal** app (search for "Terminal" with Spotlight: press ⌘ + Space).
2. Go to the Photo Cleaner folder by typing this and pressing Return:
   ```
   cd ~/photo-cleaner
   ```
3. Type the command below, then a space. Don't press Return yet:
   ```
   python3 -m photo_cleaner
   ```
4. Drag the folder of photos you want to check into the Terminal window.
   Its location will appear after the command. Now press Return.

## What you'll see

```
Photo Cleaner: checked 1,240 photos in "Phone Backup"

Found 3 groups of identical photos.

Group 1: 3 identical copies (2.1 MB each)
  Keep:          Phone Backup/2023/IMG_0012.jpg
  Extra copies:  Phone Backup/WhatsApp/IMG-20230101-WA0004.jpg
                 Phone Backup/Downloads/IMG_0012 (1).jpg
...

You could free up about 14.6 MB by removing the extra copies.
Nothing has been deleted. This is only a list.
```

- **Keep** is the oldest copy, which is most likely the original.
- **Extra copies** are files that are exactly the same, even if their names are different.
- The groups that free up the most space are shown first.
- Files are only ever read, never changed, moved or deleted.

To stop a check part-way through, press **Control + C**. Nothing will have been changed.

## Coming later

- Spotting **forwarded images** from chat apps such as WhatsApp.
- Spotting **text-heavy photos**, such as screenshots and photos of documents.

## Where this is heading

This Mac version is a prototype, built to prove that finding duplicate,
forwarded and text-heavy photos really works. The goal is a phone app for
elderly users that does the same job right on their phone. Photos will be
checked on the phone itself, so they never leave it and are never uploaded
anywhere.

## For developers

Run the automatic checks from the `photo-cleaner` folder:
```
python3 -m unittest discover tests
```
