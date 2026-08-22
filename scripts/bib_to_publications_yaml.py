#!/usr/bin/env python3
"""Generate Hugo publication YAML from the canonical BibTeX file."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to generate publication data.") from exc


RESOURCE_FIELDS: tuple[tuple[str, str], ...] = (
    ("urlpaper", "Paper"),
    ("urlpdf", "PDF"),
    ("urlarxiv", "arXiv"),
    ("urlconference", "Conference"),
    ("doi", "DOI"),
    ("urlcode", "Code"),
    ("urlgithub", "Code"),
    ("urlartifact", "Artifact"),
    ("urlslides", "Slides"),
    ("urlposter", "Poster"),
    ("urlvideo", "Video"),
    ("urlproject", "Project"),
)

SECTION_ORDER: tuple[str, ...] = ("publication", "manuscript")
SECTION_TITLES: dict[str, str] = {
    "publication": "Publications",
    "manuscript": "Manuscripts",
}
SECTION_ALIASES: dict[str, str] = {
    "publication": "publication",
    "publications": "publication",
    "published": "publication",
    "paper": "publication",
    "papers": "publication",
    "preprint": "publication",
    "preprints": "publication",
    "arxiv": "publication",
    "manuscript": "manuscript",
    "manuscripts": "manuscript",
    "unpublished": "manuscript",
    "inprogress": "manuscript",
    "work in progress": "manuscript",
    "works in progress": "manuscript",
    "thesis": "manuscript",
    "theses": "manuscript",
}

LATEX_TEXT_REPLACEMENTS = {
    r"\&": "&",
    r"\%": "%",
    r"\#": "#",
    r"\_": "_",
    r"~": " ",
}


@dataclass(frozen=True)
class BibEntry:
    entry_type: str
    key: str
    fields: dict[str, str]


def parse_bibtex(text: str) -> list[BibEntry]:
    entries: list[BibEntry] = []
    index = 0
    while True:
        start = text.find("@", index)
        if start == -1:
            break
        type_start = start + 1
        open_index = type_start
        while open_index < len(text) and text[open_index] not in "{(":
            open_index += 1
        if open_index == len(text):
            break

        entry_type = text[type_start:open_index].strip().lower()
        open_char = text[open_index]
        close_char = "}" if open_char == "{" else ")"
        body_start = open_index + 1
        depth = 1
        cursor = body_start
        while cursor < len(text) and depth > 0:
            char = text[cursor]
            if char == open_char:
                depth += 1
            elif char == close_char:
                depth -= 1
            cursor += 1

        body = text[body_start : cursor - 1]
        index = cursor
        comma = body.find(",")
        if comma == -1:
            continue
        key = body[:comma].strip()
        fields = parse_fields(body[comma + 1 :])
        if entry_type and key:
            entries.append(BibEntry(entry_type=entry_type, key=key, fields=fields))
    return entries


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    index = 0
    while index < len(text):
        while index < len(text) and text[index] in ", \n\r\t":
            index += 1
        name_start = index
        while index < len(text) and re.match(r"[A-Za-z0-9_:-]", text[index]):
            index += 1
        name = text[name_start:index].strip().lower()
        while index < len(text) and text[index].isspace():
            index += 1
        if not name or index >= len(text) or text[index] != "=":
            break
        index += 1
        while index < len(text) and text[index].isspace():
            index += 1
        value, index = parse_value(text, index)
        fields[name] = clean_bib_value(value)
    return fields


def parse_value(text: str, index: int) -> tuple[str, int]:
    if index >= len(text):
        return "", index
    if text[index] == "{":
        return parse_balanced(text, index, "{", "}")
    if text[index] == '"':
        return parse_quoted(text, index)

    start = index
    while index < len(text) and text[index] != ",":
        index += 1
    return text[start:index].strip(), index


def parse_balanced(text: str, index: int, open_char: str, close_char: str) -> tuple[str, int]:
    depth = 1
    cursor = index + 1
    while cursor < len(text) and depth > 0:
        char = text[cursor]
        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
        cursor += 1
    return text[index + 1 : cursor - 1], cursor


def parse_quoted(text: str, index: int) -> tuple[str, int]:
    cursor = index + 1
    depth = 0
    while cursor < len(text):
        char = text[cursor]
        if char == "{" and (cursor == 0 or text[cursor - 1] != "\\"):
            depth += 1
        elif char == "}" and (cursor == 0 or text[cursor - 1] != "\\"):
            depth -= 1
        elif char == '"' and depth == 0 and text[cursor - 1] != "\\":
            return text[index + 1 : cursor], cursor + 1
        cursor += 1
    return text[index + 1 : cursor], cursor


def clean_bib_value(value: str) -> str:
    value = value.strip()
    for latex, plain in LATEX_TEXT_REPLACEMENTS.items():
        value = value.replace(latex, plain)
    value = value.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", value).strip()


def display_text(value: str) -> str:
    return value.replace("---", "\u2014").replace("--", "\u2013")


def page_text(value: str) -> str:
    return value.replace("--", "-")


def numeric_or_text(value: str) -> int | str:
    return int(value) if value.isdigit() else value


def split_authors(value: str) -> list[str]:
    return [normalize_author(author) for author in re.split(r"\s+and\s+", value) if author.strip()]


def normalize_author(value: str) -> str:
    value = display_text(value.strip())
    if "," not in value:
        return value
    family, given, *_ = [part.strip() for part in value.split(",")]
    return f"{given} {family}".strip()


def publication_from_entry(entry: BibEntry) -> tuple[str, dict[str, Any]] | None:
    fields = entry.fields
    section = publication_section(entry)
    publication: dict[str, Any] = {"id": entry.key}
    if "author" in fields:
        publication["authors"] = split_authors(fields["author"])
    if "title" in fields:
        publication["title"] = display_text(fields["title"])
    if "year" in fields:
        publication["year"] = numeric_or_text(fields["year"])
    if "month" in fields:
        publication["month"] = numeric_or_text(fields["month"])
    if "day" in fields:
        publication["day"] = numeric_or_text(fields["day"])

    venue = fields.get("journaltitle") or fields.get("journal") or fields.get("booktitle")
    if venue:
        publication["journal"] = display_text(venue)
    if "pages" in fields:
        publication["pages"] = page_text(fields["pages"])
    if "publisher" in fields:
        publication["publisher"] = display_text(fields["publisher"])
    if "type" in fields:
        publication["type"] = display_text(fields["type"])
    elif entry.entry_type not in {"inproceedings", "article"}:
        publication["type"] = entry.entry_type
    status = publication_status(fields)
    if status:
        publication["status"] = status
    if "tag" in fields:
        publication["tag"] = fields["tag"]
    if "abstract" in fields:
        publication["abstract"] = display_text(fields["abstract"])

    awards = publication_awards(fields)
    if awards:
        publication["awards"] = awards
    links = publication_links(fields)
    if links:
        publication["links"] = links
    return section, publication


def publication_section(entry: BibEntry) -> str:
    fields = entry.fields
    explicit = (
        fields.get("websection")
        or fields.get("sitecategory")
        or fields.get("category")
        or fields.get("section")
    )
    if explicit:
        return normalize_section(explicit)

    for keyword in split_keywords(fields.get("keywords", "")):
        if keyword in SECTION_ALIASES:
            return SECTION_ALIASES[keyword]

    if entry.entry_type in {"thesis", "inprogress"}:
        return "manuscript"
    return "publication"


def normalize_section(value: str) -> str:
    key = value.strip().lower().replace("_", " ").replace("-", " ")
    return SECTION_ALIASES.get(key, slugify(key))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "publication"


def split_keywords(value: str) -> list[str]:
    return [keyword.strip().lower() for keyword in value.split(",") if keyword.strip()]


def publication_status(fields: dict[str, str]) -> str | None:
    if "status" in fields:
        return display_text(fields["status"])
    for keyword in split_keywords(fields.get("keywords", "")):
        if keyword not in SECTION_ALIASES:
            return display_text(keyword)
    return None


def publication_awards(fields: dict[str, str]) -> list[dict[str, str]]:
    raw_awards = fields.get("awards") or fields.get("award")
    if not raw_awards:
        return []

    labels = split_semicolon_values(raw_awards)
    urls = split_semicolon_values(fields.get("award_url") or fields.get("awardurl") or "")
    awards: list[dict[str, str]] = []
    for index, label in enumerate(labels):
        award = {"label": display_text(label)}
        if index < len(urls):
            award["url"] = urls[index]
        awards.append(award)
    return awards


def split_semicolon_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def publication_links(fields: dict[str, str]) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    resource_fields = dict(fields)
    if "urlarxiv" not in resource_fields:
        arxiv = arxiv_eprint(fields)
        if arxiv:
            resource_fields["urlarxiv"] = arxiv

    for field, default_label in RESOURCE_FIELDS:
        raw_url = resource_fields.get(field)
        if not raw_url:
            continue
        url = normalize_resource_url(field, raw_url)
        label = resource_label(fields, field, default_label)
        links.append({"label": label, "url": url})

    for field, raw_url in resource_fields.items():
        if not is_custom_url_field(field) or not raw_url:
            continue
        url = normalize_resource_url(field, raw_url)
        links.append({"label": link_field_label(field), "url": url})

    for field, raw_url in fields.items():
        if not field.startswith("link_") or not raw_url:
            continue
        url = normalize_resource_url(field, raw_url)
        links.append({"label": link_field_label(field), "url": url})
    return links


def normalize_resource_url(field: str, value: str) -> str:
    value = value.strip()
    if field in {"doi", "urldoi"}:
        return doi_url(value) or value
    if field in {"urlarxiv", "arxiv"} and not re.match(r"https?://", value):
        return arxiv_url(value) or value
    return value


def doi_url(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if re.match(r"https?://", value):
        return value
    return f"https://doi.org/{value}"


def arxiv_eprint(fields: dict[str, str]) -> str | None:
    archive = fields.get("archiveprefix") or fields.get("eprinttype")
    if not archive or archive.lower() != "arxiv":
        return None
    return fields.get("eprint")


def arxiv_url(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if re.match(r"https?://", value):
        return value
    arxiv_id = re.sub(r"^arxiv:", "", value, flags=re.IGNORECASE)
    return f"https://arxiv.org/abs/{arxiv_id}"


def link_field_label(field: str) -> str:
    label = field.removeprefix("link_").removeprefix("url")
    label = label.replace("_", " ").replace("-", " ").strip()
    if not label:
        return "Link"
    if label in {"pdf", "doi"}:
        return label.upper()
    if label == "arxiv":
        return "arXiv"
    return label.title()


def resource_label(fields: dict[str, str], field: str, default_label: str) -> str:
    stem = field.removeprefix("url")
    return (
        fields.get(f"{field}label")
        or fields.get(f"{field}_label")
        or fields.get(f"{stem}label")
        or fields.get(f"{stem}_label")
        or default_label
    )


def is_custom_url_field(field: str) -> bool:
    if not field.startswith("url") or field == "url":
        return False
    if field in {resource_field for resource_field, _ in RESOURCE_FIELDS}:
        return False
    return not (field.endswith("label") or field.endswith("_label"))


def generate(input_path: Path) -> str:
    grouped: dict[str, list[dict[str, Any]]] = {section: [] for section in SECTION_ORDER}
    extra_sections: list[str] = []
    for entry in parse_bibtex(input_path.read_text()):
        result = publication_from_entry(entry)
        if result is None:
            continue
        section, publication = result
        if section not in grouped:
            grouped[section] = []
            extra_sections.append(section)
        grouped[section].append(publication)
    for entries in grouped.values():
        entries.sort(key=publication_sort_year, reverse=True)

    section_order = list(SECTION_ORDER) + extra_sections
    sections = [
        {"id": section, "title": section_title(section), "entries": grouped[section]}
        for section in section_order
        if grouped[section]
    ]
    data = {"_tex": {"skip": True}, "sections": sections}
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=88)
    return "# Generated by scripts/bib_to_publications_yaml.py; edit assets/data/refs.bib instead.\n" + body


def publication_sort_year(publication: dict[str, Any]) -> int:
    year = publication.get("year")
    if isinstance(year, int):
        return year
    if isinstance(year, str):
        match = re.search(r"\d{4}", year)
        if match:
            return int(match.group(0))
    return -1


def section_title(section: str) -> str:
    return SECTION_TITLES.get(section, section.replace("-", " ").title())


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("assets/data/refs.bib"))
    parser.add_argument("--output", type=Path, default=Path("data/publications.yaml"))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    output = generate(args.input)
    if str(args.output) == "-":
        print(output, end="")
    else:
        args.output.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
