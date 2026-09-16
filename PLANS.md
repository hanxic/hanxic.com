# Plans

What is not done yet. Newest thinking at the top of each item; delete an item
when it ships and add a line to `RECORD.md` only if it was a real decision.

## Content

**News / announcements section.** `data/news.yaml` already exists with two
entries and is rendered nowhere (`_tex: skip: true`, no partial, no menu item).
Decide first whether this is *News* (a running list, needs feeding) or
*Recent* (three items, trimmed by hand). A stale news list is worse than none.
Placement is probably right after About, before Publications.

**Availability line.** About says who and what, not what is being sought.
One sentence — e.g. Summer 2027 research internships — if that is accurate.

**PLDG as leadership.** Service records it generically. Translate the local
title for outside readers: "Co-organizer (PLDG Czar)" plus one factual
responsibility line (speaker scheduling, communications, logistics).

**Teaching descriptions.** Every course in `data/teaching.yaml` has a
`description` field. `layouts/_partials/teaching.html` never renders it.
Either render it or drop the field.

## Layout

**Research section — what's left.** De-boxed and bracketed; see `RECORD.md`.
Still open:

- Heading hierarchy: "Current Projects" / "Selected Past Projects" are group
  labels sitting at nearly the size of the project titles beneath them. Same
  problem in Publications ("Publications" / "Manuscripts") — fix both at once,
  probably as small caps at the rail's tracking in `--ink-soft`.
- Promote `prefix`. `opOL: Oblivious Probabilistic Outcome Logic` runs the
  short name into the long one at full title weight, with a colon holding two
  different kinds of thing together. Its own line, styled like a publication's
  venue tag, would make both lists read key / title / prose / links. Only
  `opol` and `vellvm-differential-testing` have a prefix.
- Fewer brackets. Vellvm's link row is `[NFM'25] [CoqPL'25] [ICFP'24]
  [Manuscript] [Thesis]` — five in a row. But brackets are a site-wide idiom
  now doubling as the Research enclosure, so this is one decision across
  Publications and Research together, not a Research-only change.
- Check the keyword lists in `data/research_projects.yaml` — I derived them
  from the descriptions; they are claims about the work and want your eye.

**Type scale for Teaching / Service / Contact.** Four roles instead of ad-hoc
sizes, and drop weight 550:

    --type-key    0.6875rem / 600 / uppercase / 0.08em
    --type-entry  1rem      / 600
    --type-body   0.875rem  / 400
    --type-meta   0.8125rem / 400

**`max-width: 68ch`** on publication abstracts and research descriptions —
keep or drop? Currently inconsistent with the rest of the page.

## Colour

**Dark mode — parked, not rejected.** Scheme 5 "Deep Space"
(`#151a21 #1c232c #e4e8ee #98a3b3 #3fb3d4 #cf9a4f`), go **slightly bluer**
than that trial; the ground read closer to neutral black than intended.

Two blockers make this a redesign rather than a palette swap — it is the only
scheme needing work outside the PALETTE block:

- University logos (Cornell Bowers, Penn Engineering, Wharton) are dark marks
  on transparent grounds and nearly vanish. Needs light variants, or a light
  plate behind each.
- All five research figures have white backgrounds and read as lightboxes
  punched through a dark page.

Contrast targets do not survive the inversion — absolute ratios all rise. What
carries is the relationship: accent at about half the ink's ratio.

## Assets and metadata

- `assets/image/mathai.png` is 9.2 MB served at full resolution into a ~240px
  slot. `resources.Get` with no `.Resize`.
- Research figures need one aspect ratio and similar visual density; replace
  the generic Math+AI banner with an actual project visual (Lean excerpt,
  benchmark diagram, pipeline).
- `head.html` has no meta description, no canonical URL, no Open Graph or
  social card, no `Person` structured data. `static/favicon.ico` does exist.
- `research-projects.html` still emits
  `research-project-media-{{ default "default" .visual }}`. No `data/` entry
  sets `visual` and the variant CSS is gone; the hook references nothing.

## Data layer

**Theme extraction** — the last unshipped phase of the data refactor. Pull
`layouts/` and `assets/` out into a reusable Hugo theme. Deliberately left
until the shared data contract settled; it now has, so this is unblocked.

**Cruft.** `data/#research.yaml#` and `layouts/_partials/#fonts.html#` are
Emacs autosave files. `data/pulications-old.yaml` is superseded by the
generated `data/publications.yaml` (note the typo in the name). `cv/` has
LaTeX build litter (`.aux`, `.fls`, `.fdb_latexmk`, …) — gitignore it.

## CV and resume

- One-page resume: 9.5–10pt base, reached by cutting repetition rather than
  compressing further. Two variants — research/PL/formal methods, and
  compiler/systems/software engineering.
- Quantify where accurate: proof size, case studies, generated tests, bugs
  found, mentees, talks coordinated.
- Link project and experience titles to papers, code, artifacts, slides.
- Cut the Penn research-advisors line; the entries name the advisors again.
- Add Google Scholar and ORCID.
