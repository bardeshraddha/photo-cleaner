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
