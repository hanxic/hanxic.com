# Hanxi Chen Website

This repo contains my personal website, CV, and resume. The site is built with
Hugo, and the CV/resume are built with LaTeX from the same shared data used by
parts of the website.

## Repository layout

- `data/`: shared YAML data for profile, education, teaching, coursework,
  projects, service, honors, experience, research, and related site sections.
- `assets/data/refs.bib`: canonical BibLaTeX data for publications.
- `data/publications.yaml`: generated Hugo publication data, ignored by git.
- `data/research_projects.yaml`: home-page research project groupings that can
  attach publication entries by BibTeX key.
- `cv/cv.tex`: hand-authored LaTeX CV template.
- `cv/resume.tex`: hand-authored one-page LaTeX resume template.
- `scripts/yaml_to_tex_data.py`: small bridge that turns `data/*.yaml` into
  generic LaTeX macros in `cv/generated/data.tex`.
- `scripts/bib_to_publications_yaml.py`: small bridge that turns
  `assets/data/refs.bib` into Hugo publication data.
- `layouts/`: Hugo templates and partials.
- `static/cv/hanxi-chen-cv.pdf`: site-facing CV PDF generated from `cv/`.
- `static/cv/hanxi-chen-resume.pdf`: site-facing resume PDF generated from
  `cv/`.

## Editing map

Use this as the first place to decide where a change belongs:

| To edit | Main file | Also relevant |
| --- | --- | --- |
| Name, email, GitHub, LinkedIn, site handle | `data/profile.yaml` | `layouts/_partials/contact-links.html` for contact rendering |
| Home-page about text | `content/_index.md` | `layouts/_partials/about.html` for rendering |
| Header layout and nav placement | `layouts/_partials/header.html` | `layouts/_partials/menu.html`, `layouts/_partials/contact-links.html` |
| Site styling, spacing, typography, colors | `assets/css/main.css` | `static/fonts/` for vendored fonts |
| Home-page publications | `assets/data/refs.bib` | `layouts/_partials/publications.html`; generated `data/publications.yaml` should not be edited |
| Publication links, slides, code, arXiv, DOI | `assets/data/refs.bib` | Put local public files under `static/`, for example `static/slides/` |
| Home-page research projects | `data/research_projects.yaml` | `assets/image/` for project images, `layouts/_partials/research-projects.html` for rendering |
| Education | `data/education.yaml` | `layouts/_partials/education.html`, `cv/cv.tex`, `cv/resume.tex` |
| Teaching | `data/teaching.yaml` | `layouts/_partials/teaching.html`, `cv/cv.tex` |
| Service | `data/service.yaml` | `layouts/_partials/service.html`, `cv/cv.tex` |
| Honors, coursework, projects, experience | `data/honors.yaml`, `data/coursework.yaml`, `data/projects.yaml`, `data/experience.yaml` | Mostly used by `cv/cv.tex` and supporting pages |
| Research experience for CV/resume | `data/research.yaml` | `cv/cv.tex`, `cv/resume.tex`; use `resume_bullets` for shorter resume wording |
| Resume technical skills | `data/skills.yaml` | `cv/resume.tex` |
| CV layout | `cv/cv.tex` | Generated macros come from `cv/generated/data.tex` |
| Resume layout | `cv/resume.tex` | Build/install with `make resume` |
| New content pages or posts | `content/` | Hugo chooses templates from `layouts/` |
| Hugo template behavior | `layouts/` | Keep content/data in `content/`, `data/`, or `assets/data/` when possible |

## Dependencies

- Hugo
- Python 3 with PyYAML
- A LaTeX distribution with `latexmk`, BibLaTeX, and Biber

## Common commands

```sh
make
```

Refreshes the CV PDF in `static/cv/` and builds the Hugo site.

```sh
make serve
```

Starts the Hugo development server with drafts enabled.

```sh
make site
```

Regenerates `data/publications.yaml` from `assets/data/refs.bib`, then builds only the
Hugo site.

```sh
make cv
```

Regenerates the LaTeX data macros, builds the CV PDF, and copies it to
`static/cv/hanxi-chen-cv.pdf`.

```sh
make cv-pdf
```

Builds `cv/cv.pdf` without installing it into `static/cv/`.

```sh
make cv-data
```

Regenerates `cv/generated/data.tex` from `data/*.yaml`.

```sh
make resume
```

Regenerates the LaTeX data macros, builds the one-page resume PDF, and copies it
to `static/cv/hanxi-chen-resume.pdf`.

```sh
make resume-pdf
```

Builds `cv/resume.pdf` without installing it into `static/cv/`.

```sh
make publications-data
```

Regenerates `data/publications.yaml` from `assets/data/refs.bib`.

```sh
make clean
```

Removes generated CV files and Hugo's default `public/` output directory.

## Data workflow

Most structured CV and website content lives in `data/*.yaml`. LaTeX-specific
behavior should stay minimal and local to data flags such as `_tex.raw_fields`,
`_tex.join`, and `_tex.index_by`. The Python bridge should stay generic: it
should expose data to LaTeX, not decide CV layout or section semantics.

Use these files as the main editing points:

- `data/profile.yaml`: name, contact information, site handle, and CV metadata.
- `data/education.yaml`: education entries used by the Info page, CV, and
  resume.
- `data/research.yaml`: research experience for the CV and resume. The resume
  uses shorter `resume_bullets` when present.
- `data/teaching.yaml`: teaching data for the Info page and CV.
- `data/service.yaml`: service/community entries for the Info page and CV.
- `data/honors.yaml`, `data/coursework.yaml`, `data/experience.yaml`, and
  `data/projects.yaml`: CV sections and supporting structured data.
- `data/skills.yaml`: technical skills for the one-page resume.
- `data/research_projects.yaml`: home-page research project sections, text,
  images, and references.

Publication data lives in `assets/data/refs.bib`. The CV and resume read that
file directly with BibLaTeX, while Hugo reads generated `data/publications.yaml`.
The generated YAML is ignored by git; `make site`, `make serve`, and the GitHub
Pages workflow regenerate it before Hugo runs.
Put website-facing entries in one of two BibTeX keyword groups:

- `keywords = {publication}` for papers, workshop presentations, and arXiv preprints.
- `keywords = {manuscript}` for manuscripts, theses, and works in progress.

Use the normal BibTeX `url` field as the default BibLaTeX/CV URL. Website links
are generated from named URL fields such as `urlpaper`, `urlpdf`, `urlarxiv`,
`urlconference`, `urlcode`, `urlslides`, `urlproject`, and from `doi`. These
links are allowed to point to the same destination. Use labels such as
`urlpaper_label`, `urlconference_label`, or `doi_label` to override the displayed
label, or add custom fields such as `urlappendix = {https://...}`.

Research project images live in `assets/image/`. Home-page research projects use
paths relative to Hugo assets, such as `image/opol.png`, and use `refs` to attach
related publication or manuscript entries by BibTeX key from
`assets/data/refs.bib`.

Generated files should not be edited by hand. In particular,
`data/publications.yaml` comes from `assets/data/refs.bib`, and
`cv/generated/data.tex` comes from `data/*.yaml`.
