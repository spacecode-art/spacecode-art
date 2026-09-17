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
    "shipped": "✅ Shipped",
    "active": "🟡 Building",
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


def progress_bar(phases: list[dict], width: int = 24) -> str:
    total = len(phases)
    done = sum(STATUS_WEIGHT[p["status"]] for p in phases)
    filled = round(width * done / total)
    pct = round(100 * done / total)
    return f"`{'█' * filled}{'░' * (width - filled)}` **{pct}%** — phase {int(done) + 1} of {total}"


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

    shipped = sum(1 for p in phases if p["status"] == "shipped")
    adrs = sum(p.get("adrs", 0) for p in phases)
    demos = sum(1 for p in phases if p.get("demo"))
    add(
        f"**{shipped} repos shipped** &nbsp;·&nbsp; "
        f"**{adrs} architecture decision records** &nbsp;·&nbsp; "
        f"**{demos} recorded demos** &nbsp;·&nbsp; "
        f"**{profile['cloud_spend']} cloud spend**"
    )
    add("")
    add(squash(profile["summary"]))
    add("")
    add("---")
    add("")

    # --- Progress -----------------------------------------------------------
    add("## The Atlas Platform")
    add("")
    add(progress_bar(phases))
    add("")
    add("| # | Phase | Repository | What it proves | ADRs | Status |")
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
        add("### Watch it run")
        add("")
        for p in recorded:
            add(f"- **{p['name']}** — [recorded terminal session]({p['demo']})")
        add("")

    add("---")
    add("")

    # --- Reading guide ------------------------------------------------------
    add("## How to read these repositories")
    add("")
    add(
        "Every Atlas repo splits its evidence in two, and says so in its README:"
    )
    add("")
    add(
        "- **Designed & Validated** — Terraform that passes `validate` and `plan`, "
        "Terratest suites, committed Checkov/tfsec/Trivy/Semgrep output, threat "
        "models, ADRs. Permanent, reviewable, in-repo."
    )
    add(
        "- **Live Demo** — burst-deployed to real infrastructure, recorded, then "
        "`terraform destroy`d with the confirmation captured."
    )
    add("")
    add(
        "Nothing idles in a cloud account waiting for a recruiter to log in. "
        "That is a deliberate FinOps position, documented per repo with a cost "
        "model showing what the architecture *would* cost at scale — and it is "
        "the same discipline a cost-conscious team runs in production."
    )
    add("")
    add(
        "The ADR trails include the failures: emulator persistence gaps, a "
        "backend config bug that silently routed state locks to real AWS, a "
        "tooling migration forced mid-project by a vendor paywall. Real "
        "infrastructure work looks like that. The reasoning is the artifact."
    )
    add("")
    add("---")
    add("")

    # --- Principles ---------------------------------------------------------
    add("## Engineering principles")
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
    add(
        f"<sub>Generated from `data/` by `scripts/render.py` — "
        f"last updated {profile['updated']}. Do not edit this file by hand.</sub>"
    )
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