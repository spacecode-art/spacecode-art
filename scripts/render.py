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

STATUS_LABEL = {
    "shipped": "🟢 Complete",
    "active": "🟡 In progress",
    "planned": "⚪ Planned",
}
STATUS_WEIGHT = {"shipped": 1.0, "active": 0.5, "planned": 0.0}


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
        if entry["status"] not in STATUS_WEIGHT:
            sys.exit(f"error: unknown status '{entry['status']}' on {entry['repo']}")
        if entry["repo"] in seen:
            sys.exit(f"error: duplicate repo '{entry['repo']}'")
        seen.add(entry["repo"])


def squash(text: str) -> str:
    """Collapse YAML folded blocks into one table-safe line."""
    return " ".join(text.split()).replace("|", "\\|")


def progress_bar(phases: list[dict]) -> str:
    total = len(phases)
    done = sum(STATUS_WEIGHT[p["status"]] for p in phases)
    pct = round(100 * done / total)
    badge = (
        f"https://img.shields.io/badge/progress-{pct}%25-blue"
        f"?style=flat-square"
    )
    return f"![progress]({badge}) — phase {int(done) + 1} of {total}"


def repo_url(handle: str, repo: str) -> str:
    return f"https://github.com/{handle}/{repo}"


def render(profile: dict, phases: list[dict]) -> str:
    handle = profile["handle"]
    lines: list[str] = []
    add = lines.append

    # --- Header -------------------------------------------------------------
    add(f"# {profile['name']}")
    add("")
    add(f"> {squash(profile['headline'])}")
    add("")

    add(squash(profile["summary"]))
    add("")
    add(squash(profile["approach"]))
    add("")
    add("---")
    add("")

    # --- Progress -----------------------------------------------------------
    add("## The Atlas Platform")
    add("")
    add(progress_bar(phases))
    add("")
    add(
        "Phases are sequential — each repository consumes modules, policies, or "
        "telemetry from the ones before it."
    )
    add("")
    add("| # | Phase | Repository | Scope | ADRs | Status |")
    add("|---|---|---|---|---|---|")
    for p in phases:
        repo = p["repo"]
        link = f"[`{repo}`]({repo_url(handle, repo)})" if p["status"] != "planned" else f"`{repo}`"
        adr = str(p["adrs"]) if p.get("adrs") else "—"
        add(
            f"| {p['phase']} | {p['name']} | {link} | {squash(p['proves'])} "
            f"| {adr} | {STATUS_LABEL[p['status']]} |"
        )
    add("")

    # --- Evidence -----------------------------------------------------------
    recorded = [p for p in phases if p.get("demo")]
    if recorded:
        add("**Recorded sessions:** " + " &nbsp;·&nbsp; ".join(
            f"[{p['name']}]({p['demo']})" for p in recorded
        ))
        add("")

    add("---")
    add("")

    # --- Reading guide ------------------------------------------------------
    add("## What's in each repository")
    add("")
    add(
        "- **Designed and validated** — Terraform passing `validate` and `plan`, "
        "Terratest suites, committed Checkov, tfsec, Trivy, and Semgrep output, "
        "architecture diagrams, threat model, decision records."
    )
    add(
        "- **Live validation** — burst deployments to real infrastructure, "
        "recorded, with the `terraform destroy` confirmation captured alongside "
        "the run."
    )
    add("")
    add(
        "Decision records cover the problems as well as the designs — emulator "
        "persistence limits, a backend configuration bug that routed state locks "
        "to the wrong endpoint, a mid-project tooling migration after a vendor "
        "changed its free tier. Each one records what was tried, what broke, and "
        "what was decided."
    )
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
    add(f"<sub>Last updated {profile['updated']}.</sub>")
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