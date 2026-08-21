# Hanxi Chen Website

This repo contains my personal website and CV. The site is built with Hugo, and the
CV is built with LaTeX from the same shared data used by parts of the website.

## Repository layout

- `data/`: shared YAML data for profile, education, teaching, coursework,
  projects, service, honors, experience, research, and related site sections.
- `cv/refs.bib`: canonical BibLaTeX data for CV publications.
- `cv/cv.tex`: hand-authored LaTeX CV template.
- `scripts/yaml_to_tex_data.py`: small bridge that turns `data/*.yaml` into
  generic LaTeX macros in `cv/generated/data.tex`.
- `layouts/`: Hugo templates and partials.
- `static/cv/hanxi-chen-cv.pdf`: site-facing CV PDF generated from `cv/`.

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

Builds only the Hugo site.

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
make clean
```

Removes generated CV files and Hugo's default `public/` output directory.

## Data workflow

Most structured CV and website content lives in `data/*.yaml`. LaTeX-specific
behavior should stay minimal and local to data flags such as `_tex.raw_fields`,
`_tex.join`, and `_tex.index_by`. The Python bridge should stay generic: it
should expose data to LaTeX, not decide CV layout or section semantics.

Publication data for the CV lives in `cv/refs.bib` and is read directly by
BibLaTeX. Website publication data currently lives in `data/publications.yaml`
until a dedicated BibTeX-to-Hugo adapter is added.
