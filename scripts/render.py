#!/usr/bin/env python3
"""Render README.md from data/*.yml.

The README is a build artifact. Edit data/, never README.md.
Output is deterministic so `--check` can gate CI.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
README = ROOT / "README.md"

VALID_STATUSES = {"shipped", "active", "planned"}


def load(filename: str) -> dict:
    path = DATA_DIR / filename
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"error: missing data file: {path}")
    except yaml.YAMLError as exc:
        sys.exit(f"error: invalid YAML in {path}: {exc}")


def validate(phases: list[dict]) -> None:
    seen = set()
    for entry in phases:
        for field in ("phase", "name", "repo", "status", "proves"):
            if not entry.get(field):
                sys.exit(f"error: phase {entry.get('phase', '?')} missing '{field}'")
        if entry["status"] not in VALID_STATUSES:
            sys.exit(f"error: unknown status '{entry['status']}' on {entry['repo']}")
        if entry["repo"] in seen:
            sys.exit(f"error: duplicate repo '{entry['repo']}'")
        seen.add(entry["repo"])


def validate_decisions(decisions: list[dict], phases: list[dict]) -> None:
    repos = {p["repo"] for p in phases}
    for item in decisions:
        for field in ("repo", "title", "summary"):
            if not item.get(field):
                sys.exit(f"error: decision missing '{field}': {item}")
        if item["repo"] not in repos:
            sys.exit(f"error: decision references unknown repo '{item['repo']}'")


def squash(text: str) -> str:
    """Collapse YAML folded blocks into one table-safe line."""
    return " ".join(text.split()).replace("|", "\\|")


def repo_url(handle: str, repo: str) -> str:
    return f"https://github.com/{handle}/{repo}"


def decision_url(handle: str, decision: dict) -> str:
    base = repo_url(handle, decision["repo"])
    path = decision.get("path")
    return f"{base}/blob/HEAD/{path}" if path else base


def phase_table(handle: str, phases: list[dict]) -> list[str]:
    show_adrs = any(p.get("adrs") for p in phases)
    show_evidence = any(p.get("demo") for p in phases)

    headers = ["Phase", "Repository", "Scope"]
    if show_adrs:
        headers.append("ADRs")
    if show_evidence:
        headers.append("Evidence")

    rows = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for p in phases:
        repo = p["repo"]
        link = (
            f"[`{repo}`]({repo_url(handle, repo)})"
            if p["status"] == "shipped"
            else f"`{repo}`"
        )
        cells = [f"{p['phase']}. {p['name']}", link, squash(p["proves"])]
        if show_adrs:
            cells.append(str(p["adrs"]) if p.get("adrs") else "—")
        if show_evidence:
            cells.append(f"[Recording]({p['demo']})" if p.get("demo") else "—")
        rows.append("| " + " | ".join(cells) + " |")
    return rows


def render(profile: dict, phases: list[dict]) -> str:
    handle = profile["handle"]
    lines: list[str] = []
    add = lines.append

    # --- Header -------------------------------------------------------------
    add(f"# {profile['name']}")
    add("")
    add(f"**{squash(profile['headline'])}**")
    add("")
    add(squash(profile["summary"]))
    add("")
    add(squash(profile["approach"]))
    add("")
    add("---")
    add("")

    # --- Platform -----------------------------------------------------------
    add("## The Atlas Platform")
    add("")
    add(squash(profile["platform_intro"]))
    add("")
    lines.extend(phase_table(handle, phases))
    add("")
    add("---")
    add("")

    # --- Repository standard ------------------------------------------------
    add("## Repository standard")
    add("")
    add(squash(profile["standard"]["intro"]))
    add("")
    for item in profile["standard"]["items"]:
        add(f"- {item}")
    add("")
    add("---")
    add("")

    # --- Decisions ----------------------------------------------------------
    add("## Selected engineering decisions")
    add("")
    add(squash(profile["decisions_intro"]))
    add("")
    for d in profile["decisions"]:
        add(f"- **[{d['title']}]({decision_url(handle, d)})**: {squash(d['summary'])}")
    add("")
    add("---")
    add("")

    # --- Principles ---------------------------------------------------------
    add("## How I work")
    add("")
    for item in profile["principles"]:
        add(f"- {item}")
    add("")
    add("---")
    add("")

    # --- Stack --------------------------------------------------------------
    add("## Tooling")
    add("")
    for group, tools in profile["stack"].items():
        add(f"**{group}** — {' · '.join(tools)}")
        add("")
    add("---")
    add("")

    # --- Contact ------------------------------------------------------------
    add("## Contact")
    add("")
    add(" &nbsp;·&nbsp; ".join(f"[{c['label']}]({c['url']})" for c in profile["contact"]))
    add("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the profile README.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if README.md is out of date (CI gate)",
    )
    args = parser.parse_args()

    profile = load("profile.yml")
    phases = sorted(load("repos.yml")["phases"], key=lambda p: p["phase"])
    validate(phases)
    validate_decisions(profile["decisions"], phases)
    output = render(profile, phases)

    if args.check:
        current = README.read_text(encoding="utf-8") if README.exists() else ""
        if current != output:
            print("README.md is stale — run `make readme` and commit.", file=sys.stderr)
            return 1
        print("README.md is up to date.")
        return 0

    README.write_text(output, encoding="utf-8")
    print(f"wrote {README.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())