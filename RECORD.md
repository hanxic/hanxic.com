# Record

Decisions worth not re-litigating. One line each where one line will do.
Rationale lives in comments in `assets/css/main.css`; this is the index.

## Framing

A contemporary research catalogue, not a portfolio. Quietly futuristic,
minimal, recognizably academic. The tools are alignment, hierarchy, fine rules
and whitespace — not effects. No hero, no slogans, no decorative UI.

## Palette — September 2026

Five schemes trialled live; **Scheme 1 "Graphite & Signal"** chosen. A
monochrome document plus one signal.

| role | value | |
| --- | --- | --- |
| `--paper` | `#f7f0e3` | cream, H39 S56 |
| `--paper-raised` | `#fdf9f0` | |
| `--ink` | `#201d18` | warm graphite, 14.82:1 |
| `--ink-soft` | `#675f54` | 5.54:1 |
| `--accent` | `#5138c9` | indigo, 6.72:1, ΔE 94 from ink |
| `--distinction` | `#8c4a2a` | rust, 5.92:1 |

Rules any future scheme must satisfy:

- `--ink` clears 7:1 on the paper.
- `--accent` lands near **6.5:1 — a band, not a floor** — *and* ΔE 20+ from
  `--ink`. ΔE makes a link noticeable (ΔE 12 is invisible at 15px); contrast
  places it. Above ~7:1 an accent stops being a mark on the prose and becomes
  a second body colour. 7.29:1 was trialled and rejected for this.
- Hover always raises contrast: chrome links climb to the accent, accent links
  settle into the ink.

The paper went neutral `#f2f3f5` → `#f4f1eb` → cream `#f7f0e3`. Warming it past
~S40 forced the ink to follow: a cool graphite on a cream ground reads visibly
blue, because the eye judges ink against paper, not absolutely. Ink and
ink-soft moved to hue ~38, which makes `--accent` the only cool thing on the
page — a stronger signal than being merely the only saturated one.
`--distinction` had to move furthest (amber H35 disappeared into the warmed
paper; rust H20 does not).

**All colour lives in the `:root` PALETTE block and nowhere else** — verified
by scanning below `:root` for `#hex`, `rgb()`, `rgba()`, `hsl()`: zero hits. A
scheme swap is seven lines. `--ink-rgb` / `--accent-rgb` must be kept in step
by hand; CSS cannot decompose a hex. Getting there meant deleting 144 lines of
dead `.research-project-media-*` CSS (recoverable from git).

Superseded: navy/blue `#2a4568` + `#0a5ca3` with a purple `#4e3269` secondary,
and the `#0070ba` link-contrast fix that went with it.

## Type and colour of text

- Iosevka throughout. Body 0.9375rem desktop / 0.875rem phone, line height 1.4;
  prose 1rem / 1.48.
- The name is the page's only typographic climax: `clamp(1.75rem, 1.05rem +
  3.1vw, 2.5rem)`, ~2.7× prose. It can be, because it is not sticky.
- Author lines and dead refs (`[Manuscript]`, `[Thesis]`) both sit at
  `--ink-soft`; that shade means one thing — supporting detail. Titles are the
  only full-ink line in an entry. *Authors at full ink was trialled and
  reverted: two equally loud lines, nothing to enter the entry by.*
- `.myname` is bold and nothing else. Weight is one difference; weight plus
  colour made the list read as two classes of person.

## Header

Split in two, because a contact row you need once was paying rent in the
sticky strip.

- **`.site-masthead`** — name left, contacts right, one baseline, scrolls away.
  Contacts are lowercase middot-separated links; brackets belong to the
  section index alone.
- **`.site-index`** — the only sticky chrome, one line. Sticky offset fell
  ~96px → 50px. Carries the same `01`–`06` numbers as the section rail, so
  header and rail read as one system. The name reappears here as a small mark
  only once the masthead has actually left (IntersectionObserver with
  `rootMargin` = strip height); below 860px it is dropped entirely.
- Menu weights in `hugo.toml` must stay in the same order as the partials in
  `layouts/home.html` — the menu numbers by position, the rail by CSS counter.
- `--sticky-header-offset` is resampled by `ResizeObserver` + `document.fonts.
  ready`, not just on load/resize; it went stale when the webfont swapped in.

## Sections

- **Closing rule.** Every section ends the same measure below its last line of
  ink, not below its last *box*. A row is padded to sit centred between two
  rules; the last row has no rule beneath it, so that padding was surplus and
  each section closed at a different distance (14px in Publications, 43px in
  Service). `--row-pad` is declared once per section and read twice — by the
  rows, and by `.section`'s `padding-bottom: calc(... - var(--row-pad, 0rem))`.
  *Superseded: `#publications { padding-bottom: 0 }`, a hand-tuned fix for one
  section that over-corrected.*
- **Rail numbering.** A position index, not an accent: label tracking, no
  leading zero, `--ink-soft`, short keyline left of every section. The section
  in view takes the accent, driven by the existing scroll-spy.
- **Publications.** Fading hairline separator (chosen over inset hairline,
  short accent rule, left keyline, whitespace-only — never combine two).
  Abstracts use native `<details>` with a plus/minus cue and a 280ms slide;
  reduced-motion gets an instant toggle.
- **Research.** Bracketed, not boxed. An entry is a composite — title,
  keywords, prose, figure — so unlike every other list it does want an
  enclosure; it just doesn't want a card. Keeping one side in four leaves a
  bracket pair, which is this page's own punctuation (`[About]`, `[DOI]`,
  `[NFM'25]`) at display size: native rather than borrowed, and a fifth of the
  ink. Hairline at rest, accent and wider on hover and `focus-within` — the
  page's one piece of instrumentation, and the reason the mark is drawn with
  borders, which animate, rather than gradients, which don't. Figure is
  top-aligned so the entries share a horizon. A three-term keyword strip
  (`LEAN 4 · PROGRAM LOGIC · PROBABILISTIC`) places the work for readers
  outside PL. *Superseded: the tinted gradient, shadow, rounded corners, inner
  media divider, then the flat bordered panel that replaced them; also a plain
  de-box to shared row rules, which was correct and boring.*
  - The brackets live on the `<article>`, the columns on a `div` inside it.
    They cannot share an element: an absolutely positioned pseudo-element of a
    grid container resolves against its grid area, not the padding box, so
    paired `top`/`bottom` collapse it to its arms.
- **Education.** Its own section. Institution and degree lines carry the
  hierarchy; GPA, advisors and honors read as compact prose, not a grid. Real
  logo colours, no cards or shadows. `/info/` redirects here.
- **Teaching / Service.** Text-led ledgers, not cards. Course codes in a quiet
  left column, aligned role/date columns, no brackets. Slightly smaller than
  Education and Publications to signal a supporting role.
- **Contact.** Same rail and hairline rows as Service — a catalogue entry, not
  a call to action. Phone stays out of the web build (CV only).

## Data layer

The site and the LaTeX CV share one canonical data layer. Shipped; the only
remaining phase is theme extraction.

- **YAML is canonical** for profile/CV/site data, **BibTeX** for publications
  (`assets/data/refs.bib`, with nonstandard `url*`/`tag`/`award` fields and
  `keywords` grouping entries as `publication` or `manuscript`).
- Data files are **root maps with an `entries` key**, not root lists, so there
  is a stable place for metadata and flags.
- `_tex:` is the reserved key for serialization flags (`skip`, `raw_fields`,
  `url_fields`, `join`, `index_by`). Flags may affect access and escaping;
  **presentation never goes here** — it belongs in `cv.tex` or a Hugo template.
- Two small adapters, both schema-agnostic on purpose:
  `scripts/yaml_to_tex_data.py` → `cv/generated/data.tex` (flat `\CVSet`
  macros, `\input` by both `cv.tex` and `resume.tex`), and
  `scripts/bib_to_publications_yaml.py` → `data/publications.yaml`. LaTeX
  reads the `.bib` directly; only Hugo needs the adapter.
- Neither generator knows what "education" or "teaching" mean, and neither
  emits LaTeX sections. LaTeX owns CV typography, Hugo owns site layout.

## Rejected

- A standfirst above the About prose — repeated the first paragraph.
- Research panels as dashboard cards (three depth cues at once).
- Filters, illustrations, animation added for its own sake.
