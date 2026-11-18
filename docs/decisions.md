# Decision Log

A record of the important choices made in this project and why we made them.
New decisions go at the bottom.

Each entry has:
- **Date:** when the decision was made
- **Decision:** what we decided
- **Why:** the reason
- **Alternatives considered:** other options, and why we didn't pick them
- **Revisit when:** what would make us think again

---

## 1. Never delete files, only list them

- **Date:** 23 Oct 2026
- **Decision:** The tool only lists photos that could be removed and how much space that
  would free. It never deletes, moves, renames or changes any file. The person decides
  what to do.
- **Why:** Our users are elderly. Losing a precious photo by mistake would be far worse
  than keeping a few extra copies. A list is always safe, and it builds trust.
- **Alternatives considered:**
  - *Delete automatically:* fastest, but one mistake could lose a photo forever.
  - *Delete after the person confirms:* still risky. People often tap "Yes" without reading.
  - *Move extra copies to a "review" folder:* safer, but files still get moved around, which
    can confuse people and break albums.
- **Revisit when:** users clearly trust the results and ask for help removing photos. Even then,
  use the phone's own "Recently Deleted" bin so anything can be recovered.

## 2. On-device processing by default, no uploading photos

- **Date:** 23 Oct 2026
- **Decision:** Photos are checked on the person's own device. They are never uploaded to
  the internet or sent to an online service.
- **Why:** Photos are deeply personal. Keeping them on the device protects privacy, works
  without an internet connection, and is easy to explain to users and their families:
  "your photos never leave your phone."
- **Alternatives considered:**
  - *Online (cloud) processing:* more computing power for harder tasks such as reading text
    in photos, but it means uploading private photos, needs an internet connection, and
    costs money to run.
- **Revisit when:** a feature truly can't run well on a phone. Even then, it should be optional,
  clearly explained, and switched off unless the person turns it on.

## 3. Build a Mac prototype first, phone app later

- **Date:** 23 Oct 2026
- **Decision:** Build a small Python tool on a Mac to prove that detecting duplicates,
  forwarded images and text-heavy photos actually works. The final product is a phone
  app for elderly users.
- **Why:** Testing ideas on a Mac is much quicker and cheaper than building a phone app.
  We learn which detection methods work before spending time on screens and app stores.
- **Alternatives considered:**
  - *Build the phone app straight away:* we'd get to the real product sooner, but every
    change would be slower, and we might build screens for detection that doesn't work.
- **Revisit when:** all three kinds of detection work well on the Mac, or a detection method
  turns out to be impossible on a phone.

## 4. Start with exact duplicates, even though the iPhone already finds them

- **Date:** 24 Oct 2026
- **Decision:** Milestone 1 finds exact duplicate photos, even though the iPhone's Photos app
  already has a "Duplicates" feature.
- **Why:** It's the simplest useful step. It sets up the project's foundations (finding photos,
  friendly reports, automatic checks, the never-delete rule) without needing any add-ons.
  The real value of this product is in the later milestones, forwarded images and
  text-heavy photos, which the iPhone doesn't offer.
- **Alternatives considered:**
  - *Start with forwarded images or text-heavy photos:* more valuable to users, but harder,
    and they need extra add-ons, so there's more to go wrong on day one.
  - *Skip duplicates entirely:* saves time, but we'd lose a simple, reliable first step
    to build on.
- **Revisit when:** planning the phone app. Duplicates may not need to be a main feature there,
  since the iPhone already handles it. It could become a small extra, or be left out.

## 5. When copies have the same date, keep the one with the "original" name

- **Date:** 18 Nov 2026
- **Decision:** We still suggest keeping the oldest copy. But when copies have exactly the
  same date, we prefer the one whose name doesn't look like a copy (such as "copy",
  "copy 2", "(1)" or "Copy of ..."). If that still doesn't decide it, we prefer the
  shorter name.
- **Why:** Testing on a real folder (the Maui photoshoot) suggested keeping
  "shraddha 3 copy.jpg" and removing "shraddha 3.jpg". Both had the same date, so the
  tool fell back to alphabetical order, which put the "copy" first. That looks backwards
  and could confuse or worry our users.
- **Alternatives considered:**
  - *Alphabetical order only (what we had):* simple, but it gave the confusing result above.
  - *Decide by name only, ignoring dates:* a renamed original (like "Grandma's birthday.jpg")
    could lose to a newer copy with a plainer name. The date is a stronger clue.
  - *Also treat names ending in "-1" as copies:* rejected, because ordinary names like
    "Holiday-2023.jpg" would be mistaken for copies.
- **Revisit when:** we see other copy-naming patterns in real folders (for example from
  Google downloads, WhatsApp or phones), or when building the phone app, where the
  phone's photo library gives its own dates.

## 6. Spot forwarded pictures mainly by missing camera details and small size

- **Date:** 18 Nov 2026
- **Decision:** A picture is "probably from a chat app" when it has no camera details
  (no camera make or model, no date taken) *and* its longest side is 1,600 pixels or less.
  It is "very likely" when its name, its folder, or its hidden "made by" label points to
  a chat or social media app (for example "IMG-…-WA0004.jpg", a "WhatsApp Images" folder,
  or "Instagram").
- **Why:** Chat apps remove camera details and shrink pictures when sending. On an iPhone,
  saved pictures get ordinary names like "IMG_1234.JPG", so names alone won't work in the
  phone app, but missing camera details will. Both clues are needed together: the Maui
  photoshoot photos had no camera details either, but they are far too big to be from a chat app.
- **Alternatives considered:**
  - *File names only:* very reliable when present, but they disappear on an iPhone.
  - *Missing camera details only:* would wrongly flag all 176 Maui photos.
  - *Treat the "Picasa" label as a WhatsApp clue:* seen on a real WhatsApp picture, but not
    confirmed, and real Picasa users could have it on their own photos. Left out for now.
- **Revisit when:** we have a real WhatsApp "HD" picture (up to 4,096 pixels, which the size
  rule won't catch), or we find pictures the rules get wrong.

## 7. Skip HEIC and PNG files when looking for forwarded pictures

- **Date:** 18 Nov 2026
- **Decision:** The chat-app check only looks at JPG and WebP pictures.
- **Why:** HEIC is the iPhone camera's own format, and chat apps convert pictures to JPG before
  sending, so HEIC files are almost always the person's own photos. PNG files are mostly
  screenshots, which belong to Milestone 3. This also avoids a second add-on for reading HEIC.
- **Alternatives considered:**
  - *Check every kind of picture:* more complete, but screenshots would flood the list, and
    reading HEIC needs another add-on.
- **Revisit when:** building Milestone 3 (decide where screenshots belong), or if we find chat
  apps that send HEIC or PNG.

## 8. List all chat-app pictures, with a gentle warning

- **Date:** 18 Nov 2026
- **Decision:** The report lists every picture that seems to come from a chat app or social
  media, with the reason for each, and warns that some may be precious family photos.
- **Why:** The tool can't tell a forwarded "Good morning" greeting from a grandchild's photo sent
  on WhatsApp. Our real test proved it: a family photo and an Instagram picture looked almost
  the same to the tool. Showing everything with a clear warning keeps the person in charge.
- **Alternatives considered:**
  - *Wait for Milestone 3 and list only text-heavy pictures:* safer, but misses forwarded
    clutter that has no text.
  - *Leave out "probably" pictures:* fewer mistakes, but would also miss family-sized clutter.
- **Revisit when:** Milestone 3 can spot greetings and memes. Then those could be shown
  separately from pictures that might be family photos.

## 9. Skip the Mac Photos Library when checking a folder

- **Date:** 18 Nov 2026
- **Decision:** When checking a folder, the tool doesn't go inside any Photos app library
  (folders ending in ".photoslibrary"). Pointing the tool directly at the library's
  "originals" folder still works.
- **Why:** Checking the whole Pictures folder flagged 2,416 pictures as "from chat apps". All
  of them were the Photos app's own small preview copies inside its library. They aren't real
  photos, and people shouldn't be encouraged to touch files inside the library, which can
  damage it.
- **Alternatives considered:**
  - *Check the library's "originals" folder automatically:* useful, but most originals may be
    in iCloud anyway, and the Photos app is better at managing its own photos.
- **Revisit when:** building the phone app, which will read the phone's photo library through
  the phone's own tools rather than as files.
