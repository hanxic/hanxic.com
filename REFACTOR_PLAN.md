# Refactor Plan: Shared CV Data and Website Theme Preparation

## Goal

Reorganize the repository so the personal website and LaTeX CV share one canonical data layer, while keeping the Hugo site and CV template easy to maintain. Theme extraction should come later, after the shared data contract settles.

## Guiding Principles

- Keep data canonical in formats that fit the data.
- Do not force every source file into YAML.
- Keep LaTeX responsible for typography and CV layout.
- Keep Hugo responsible for website layout.
- Keep generators small, boring, and schema-agnostic.
- Use generated files only as adapters between canonical data and output formats.

## Canonical Sources

Use YAML for structured profile/CV/site data:

- `data/profile.yaml`
- `data/education.yaml`
- `data/teaching.yaml`
- `data/research.yaml`
- `data/projects.yaml`
- `data/honors.yaml`
- `data/coursework.yaml`
- `data/service.yaml`
- `data/experience.yaml`
- `data/news.yaml`

Use BibTeX/BibLaTeX for publications:

- `cv/refs.bib`

The BibTeX file may include extra nonstandard fields for richer website output, such as:

- `url`
- `doi`
- `arxiv`
- `pdf`
- `code`
- `slides`
- `project`
- `artifact`
- `tag`
- `showweb`
- `showcv`

## Data File Shape

Prefer root maps rather than root lists when a file may need metadata or flags.

Example:

```yaml
_tex:
  index_by: id

entries:
  - id: cornell
    school: Cornell University
    location: Ithaca, NY
```

Hugo would read this as:

```go-html-template
{{ range .Site.Data.education.entries }}
```

The root map gives us a stable place for metadata like `_tex`, future theme configuration, or visibility rules.

## LaTeX Data Bridge

Generate a generic TeX data database from YAML:

```text
data/*.yaml -> scripts/yaml_to_tex_data.py -> cv/generated/data.tex
```

The generator should emit schema-agnostic access macros, for example:

```tex
\CVSet{education.entries.1.school}{Cornell University}
\CVSet{education.entries.1.degrees.1.title}{Ph.D. in Computer Science}
\CVSetLen{education.entries}{2}
\CVSetLen{education.entries.1.degrees}{1}
\CVSetKeys{education.entries.1}{id,school,location,degrees}
```

Then `cv/cv.tex` owns the semantic rendering:

```tex
\School{\CVData{education.entries.1.school}}{\CVData{education.entries.1.location}}\\
\Degree{\CVData{education.entries.1.degrees.1.title}}{\CVData{education.entries.1.cv_years}}
```

This keeps the generator from becoming a second CV template.

## `_tex` Flags

Use `_tex` as a reserved YAML key for generic serialization flags. These flags may affect access or escaping, but should not define presentation.

Good flags:

```yaml
_tex:
  skip: true
  skip_fields:
    - private_note
  raw_fields:
    - cv_number
  url_fields:
    - url
    - website
  join:
    numbers: " / "
    terms: ", "
  index_by: id
```

Generated convenience values might include:

```tex
\CVData{teaching.entries.1.courses.1.numbers.@joined}
\CVData{education.by_id.cornell.school}
\CVData{education.@ids}
```

Avoid presentation flags such as:

```yaml
_tex:
  render_as: two_column_honors
```

Presentation should stay in `cv/cv.tex` or Hugo templates.

## CV Build

Keep `cv/cv.tex` as a hand-authored LaTeX template.

It should:

- `\input{generated/data.tex}` for YAML-derived data.
- Use `refs.bib` directly through BibLaTeX.
- Define the CV typography, spacing, section order, loops, and rendering macros.

Build flow:

```text
data/*.yaml
  -> cv/generated/data.tex
  -> cv/cv.tex
  -> cv/cv.pdf
  -> static/cv/hanxi-chen-cv.pdf

cv/refs.bib
  -> BibLaTeX inside cv/cv.tex
```

## Website Build

Hugo should read YAML directly from `data/*.yaml`.

Website publications can initially continue to use `data/publications.yaml`. Later, if desired, add a small one-purpose adapter:

```text
cv/refs.bib -> data/publications.yaml
```

That adapter should only translate publication metadata for Hugo; it should not participate in the LaTeX CV build.

## Implementation Phases

1. Normalize data files into root maps with `entries`, `groups`, or other clear top-level keys.
2. Add the generic YAML-to-TeX data serializer.
3. Add `cv/generated/data.tex` to the CV build as a generated artifact.
4. Rewrite `cv/cv.tex` as a hand-authored template that reads the generated data macros and `refs.bib`.
5. Update Hugo partials to use the normalized data shapes.
6. Build and verify both outputs:
   - LaTeX CV PDF
   - Hugo site
7. After the shared data contract stabilizes, extract the Hugo layouts/assets into a reusable theme.

## Non-Goals for This Step

- Do not extract the Hugo theme yet.
- Do not make LaTeX parse YAML directly.
- Do not generate full LaTeX sections from Python.
- Do not make the generator understand domain concepts like education, teaching, or research.
