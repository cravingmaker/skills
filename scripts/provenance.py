"""Validate declared per-file provenance, not the completeness of source attribution."""

import csv
import io
import re
from pathlib import Path

COLUMNS = ("source", "source_url", "source_path", "source_revision", "sha256", "license",
           "copyright_holders", "destination_paths", "kept_material", "local_changes",
           "license_files", "notice_files")
REVISION = re.compile(r"[0-9a-f]{40}")
HASH = re.compile(r"[0-9a-f]{64}")


def manifest_rows(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".csv":
        reader = csv.DictReader(io.StringIO(text))
        if tuple(reader.fieldnames or []) != COLUMNS:
            raise ValueError("CSV header must be " + ",".join(COLUMNS))
        rows = list(reader)
        if any(None in row or any(value is None for value in row.values()) for row in rows):
            raise ValueError("every CSV row must have exactly the manifest columns")
    else:
        if not text.startswith("# Sources\n"):
            raise ValueError("references/SOURCES.md must start with '# Sources'")
        tables = []
        for block in re.findall(r"(?:^\|.*\n)+", text, re.M):
            lines = block.strip().splitlines()
            fields = [part.strip() for part in lines[0].strip("|").split("|")]
            if tuple(fields) != COLUMNS:
                continue
            if len(lines) < 3 or not re.fullmatch(r"[| :\-]+", lines[1]):
                raise ValueError("the manifest needs a table separator and at least one source-file row")
            table = []
            for line in lines[2:]:
                values = [value.strip() for value in line.strip("|").split("|")]
                if len(values) != len(COLUMNS):
                    raise ValueError("each Markdown manifest row must have exactly twelve columns")
                table.append(dict(zip(COLUMNS, values)))
            tables.append(table)
        if len(tables) != 1:
            raise ValueError("references/SOURCES.md needs one table with the twelve manifest columns in order")
        rows = tables[0]
    if not rows:
        raise ValueError("the source manifest needs at least one retained source-file row")
    return rows


def local_file(directory: Path, value: str) -> Path:
    relative = Path(value)
    path = directory / relative
    if relative.is_absolute() or ".." in relative.parts or not path.resolve().is_relative_to(directory.resolve()):
        raise ValueError(f"{value}: use a local path within this skill")
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"{value}: declared provenance file is missing or not a regular owned file")
    return path


def check(directory: Path, metadata: dict, is_source_url) -> list[str]:
    source = metadata.get("source")
    if source is None:
        return []
    problems = []
    for key in ("source-files", "local-changes"):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            problems.append(f"adapted skills need non-empty string metadata.{key}")
    body = (directory / "SKILL.md").read_text(encoding="utf-8")
    linked = [name for name in ("references/SOURCES.md", "references/sources.csv") if re.search(r"\]\(" + re.escape(name) + r"\)", body)]
    if len(linked) != 1:
        return problems + ["link one per-file manifest, references/SOURCES.md or references/sources.csv, directly from SKILL.md"]
    try:
        path = local_file(directory, linked[0])
        rows = manifest_rows(path)
    except (OSError, ValueError) as error:
        return problems + [f"source manifest: {error}"]
    primary, seen = [], set()
    for index, row in enumerate(rows, 1):
        try:
            for key in COLUMNS:
                if not isinstance(row[key], str) or (not row[key].strip() and key != "notice_files"):
                    raise ValueError(f"{key} must be non-empty (use none only for notice_files)")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", row["source"]):
                raise ValueError("source must be a canonical contributor identifier")
            if not is_source_url(row["source_url"]):
                raise ValueError("source_url must be one absolute upstream URL")
            if not REVISION.fullmatch(row["source_revision"]):
                raise ValueError("source_revision must be a full 40-character SHA")
            if not HASH.fullmatch(row["sha256"]):
                raise ValueError("sha256 must be an exact 64-character lowercase byte hash")
            if Path(row["source_path"]).is_absolute() or ".." in Path(row["source_path"]).parts:
                raise ValueError("source_path must be relative to its pinned upstream tree")
            identity = (row["source"], row["source_url"], row["source_revision"], row["source_path"])
            if identity in seen:
                raise ValueError("duplicate source-file row; combine its destination_paths")
            seen.add(identity)
            destinations = [part.strip() for part in row["destination_paths"].split(";")]
            for value in destinations:
                local_file(directory, value)
            licenses = [part.strip() for part in row["license_files"].split(";")]
            if f"LICENSE-{row['source']}" not in licenses:
                raise ValueError(f"every contributor needs its own LICENSE-{row['source']} in license_files")
            legal_text = []
            for value in licenses:
                if not value.startswith("LICENSE-") or "/" in value:
                    raise ValueError("license_files must name root LICENSE-<upstream> files")
                text = local_file(directory, value).read_text(encoding="utf-8")
                # The header precedes the original complete legal text.
                header = re.split(r"\n(?:MIT License|Apache License|Copyright)", text, maxsplit=1)[0]
                if not re.search(r"Adapted (?:material|files):", header) or any(destination not in header for destination in destinations):
                    raise ValueError(f"{value}: header must name every adapted local file under 'Adapted files:' or 'Adapted material:'")
                legal_text.append(text)
            for holder in row["copyright_holders"].split(";"):
                if holder.strip() not in "\n".join(legal_text):
                    raise ValueError(f"copyright holder {holder.strip()} is absent from declared legal files")
            notices = [] if row["notice_files"].strip() in ("", "none") else row["notice_files"].split(";")
            for value in notices:
                if not Path(value.strip()).name.startswith("NOTICE"):
                    raise ValueError("notice_files must name NOTICE files")
                local_file(directory, value.strip())
            if "Apache-2.0" in row["license"] and not notices:
                raise ValueError("Apache-2.0 contributions need their applicable NOTICE in notice_files")
            if row["source_url"] == source and row["source_revision"] == metadata.get("source-revision"):
                primary.append(row["source_path"])
        except (OSError, ValueError) as error:
            problems.append(f"source manifest row {index}: {error}")
    if not primary:
        problems.append("source manifest must include the primary metadata.source and source-revision")
    declared = metadata.get("source-files", "")
    if isinstance(declared, str) and set(declared.split()) - set(primary):
        problems.append("metadata.source-files must match primary retained source paths in the manifest")
    return problems
