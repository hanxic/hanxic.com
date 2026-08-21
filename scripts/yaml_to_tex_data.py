#!/usr/bin/env python3
"""Serialize YAML data files into a small TeX key-value database."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to generate TeX data.") from exc


URL_FIELD_NAMES = {
    "arxiv",
    "artifact",
    "code",
    "doi",
    "github",
    "linkedin",
    "pdf",
    "project",
    "slides",
    "url",
    "website",
}

LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "%": r"\%",
    "#": r"\#",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

UNICODE_REPLACEMENTS = {
    "\u2013": "--",
    "\u2014": "---",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": "``",
    "\u201d": "''",
}


@dataclass(frozen=True)
class TexOptions:
    skip_fields: frozenset[str] = field(default_factory=frozenset)
    raw_fields: frozenset[str] = field(default_factory=frozenset)
    url_fields: frozenset[str] = field(default_factory=lambda: frozenset(URL_FIELD_NAMES))
    joins: dict[str, str] = field(default_factory=dict)

    def merge(self, config: dict[str, Any]) -> "TexOptions":
        return TexOptions(
            skip_fields=self.skip_fields | as_name_set(config.get("skip_fields")),
            raw_fields=self.raw_fields | as_name_set(config.get("raw_fields")),
            url_fields=self.url_fields | as_name_set(config.get("url_fields")),
            joins={**self.joins, **as_string_map(config.get("join"))},
        )


def as_name_set(value: Any) -> frozenset[str]:
    if value is None:
        return frozenset()
    if isinstance(value, str):
        return frozenset([value])
    if isinstance(value, Iterable):
        return frozenset(str(item) for item in value)
    raise TypeError(f"expected a string or list of strings, got {type(value).__name__}")


def as_string_map(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise TypeError(f"expected a map, got {type(value).__name__}")
    return {str(key): str(item) for key, item in value.items()}


def tex_config(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    config = value.get("_tex", {})
    if config is None:
        return {}
    if not isinstance(config, dict):
        raise TypeError("_tex must be a map")
    return config


def stringify_scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def tex_escape(value: Any) -> str:
    text = stringify_scalar(value)
    for old, new in UNICODE_REPLACEMENTS.items():
        text = text.replace(old, new)
    return "".join(LATEX_SPECIALS.get(char, char) for char in text)


def tex_escape_url(value: Any) -> str:
    text = stringify_scalar(value)
    text = text.replace("\\", "/")
    text = text.replace("{", r"\{").replace("}", r"\}")
    text = text.replace("%", r"\%").replace("#", r"\#")
    return rf"\url{{{text}}}"


def tex_value(value: Any, options: TexOptions, field_name: str | None) -> str:
    if field_name in options.raw_fields:
        return stringify_scalar(value)
    if field_name in options.url_fields:
        return tex_escape_url(value)
    return tex_escape(value)


def path_text(path: list[str]) -> str:
    return ".".join(path)


def is_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def alias_segment(value: Any) -> str:
    text = stringify_scalar(value).strip()
    text = re.sub(r"[^A-Za-z0-9_:-]+", "-", text)
    text = text.strip("-")
    return text or "item"


class Emitter:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def set(self, path: list[str], value: Any, options: TexOptions, field_name: str | None) -> None:
        self.lines.append(rf"\CVSet{{{path_text(path)}}}{{{tex_value(value, options, field_name)}}}")

    def set_len(self, path: list[str], length: int) -> None:
        self.lines.append(rf"\CVSetLen{{{path_text(path)}}}{{{length}}}")

    def set_keys(self, path: list[str], keys: list[str]) -> None:
        self.lines.append(rf"\CVSetKeys{{{path_text(path)}}}{{{','.join(keys)}}}")

    def walk(self, path: list[str], value: Any, options: TexOptions, field_name: str | None = None) -> None:
        config = tex_config(value)
        if config.get("skip", False):
            return
        options = options.merge(config)

        if isinstance(value, dict):
            items = [
                (str(key), item)
                for key, item in value.items()
                if key != "_tex" and str(key) not in options.skip_fields
            ]
            self.set_keys(path, [key for key, _ in items])
            for key, item in items:
                self.walk(path + [key], item, options, key)
            self.emit_indexes(path, value, options, config)
            return

        if isinstance(value, list):
            self.set_len(path, len(value))
            if field_name in options.joins and all(is_scalar(item) for item in value):
                joined = options.joins[field_name].join(stringify_scalar(item) for item in value)
                self.set(path + ["@joined"], joined, options, field_name)
            for index, item in enumerate(value, start=1):
                self.walk(path + [str(index)], item, options, field_name)
            return

        if is_scalar(value):
            self.set(path, value, options, field_name)
            return

        raise TypeError(f"unsupported value at {path_text(path)}: {type(value).__name__}")

    def emit_indexes(
        self,
        path: list[str],
        value: dict[str, Any],
        options: TexOptions,
        config: dict[str, Any],
    ) -> None:
        for list_name, id_field in index_targets(value, config):
            items = value.get(list_name)
            if not isinstance(items, list):
                continue

            ids: list[str] = []
            for index, item in enumerate(items, start=1):
                if not isinstance(item, dict) or id_field not in item or not is_scalar(item[id_field]):
                    continue
                item_id = alias_segment(item[id_field])
                ids.append(item_id)
                if list_name == "entries":
                    alias_path = path + ["by_id", item_id]
                else:
                    alias_path = path + [list_name, "by_id", item_id]
                self.walk(alias_path, item, options, None)

            if ids:
                if list_name == "entries":
                    ids_path = path + ["@ids"]
                else:
                    ids_path = path + [list_name, "@ids"]
                self.set(ids_path, ",".join(ids), options, None)


def index_targets(value: dict[str, Any], config: dict[str, Any]) -> list[tuple[str, str]]:
    index_by = config.get("index_by")
    if isinstance(index_by, str):
        return [("entries", index_by)] if isinstance(value.get("entries"), list) else []
    if isinstance(index_by, dict):
        return [(str(list_name), str(id_field)) for list_name, id_field in index_by.items()]
    return []


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def generate(data_dir: Path) -> str:
    emitter = Emitter()
    options = TexOptions()

    for path in sorted(data_dir.glob("*.yaml")):
        data = load_yaml(path)
        if data is None:
            continue
        emitter.walk([path.stem], data, options)

    header = [
        "% Generated by scripts/yaml_to_tex_data.py; do not edit.",
        r"\makeatletter",
        r"\providecommand{\CVSet}[2]{\expandafter\gdef\csname cvdata@#1\endcsname{#2}}",
        r"\providecommand{\CVData}[1]{\@ifundefined{cvdata@#1}{}{\csname cvdata@#1\endcsname}}",
        r"\providecommand{\CVSetLen}[2]{\CVSet{#1.@len}{#2}}",
        r"\providecommand{\CVLen}[1]{\CVData{#1.@len}}",
        r"\providecommand{\CVSetKeys}[2]{\CVSet{#1.@keys}{#2}}",
        r"\providecommand{\CVKeys}[1]{\CVData{#1.@keys}}",
        r"\makeatother",
        "",
    ]
    return "\n".join(header + emitter.lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("cv/generated/data.tex"))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    output = generate(args.data_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
