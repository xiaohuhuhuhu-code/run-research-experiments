#!/usr/bin/env python3
"""Check whether comparable experiment runs use consistent settings.

This script is intentionally dependency-free. It accepts either a simple
YAML registry matching templates/experiment_registry.yaml or a JSON file
containing {"runs": [...]}.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


HARD_FIELDS = [
    "epochs",
    "batch_size",
    "split",
    "input_size",
    "eval_script",
    "seed_policy",
    "precision",
    "gradient_accumulation",
]


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "None", "~"}:
        return None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def load_simple_yaml(path: Path) -> dict[str, Any]:
    runs: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    section_stack: list[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if stripped == "runs:":
            section_stack = ["runs"]
            continue

        if stripped.startswith("- "):
            if current:
                runs.append(current)
            current = {}
            item = stripped[2:].strip()
            if item and ":" in item:
                key, value = item.split(":", 1)
                current[key.strip()] = parse_scalar(value)
            continue

        if current is None or ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        # Keep nested dictionaries simple: metrics.foo and artifacts.foo.
        if value == "":
            section_stack = [key]
            continue
        if indent >= 6 and section_stack:
            current[f"{section_stack[-1]}.{key}"] = parse_scalar(value)
        else:
            current[key] = parse_scalar(value)

    if current:
        runs.append(current)
    return {"runs": runs}


def load_registry(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.startswith("{") or text.startswith("["):
        data = json.loads(text)
        if isinstance(data, list):
            return data
        return data.get("runs", [])
    return load_simple_yaml(path).get("runs", [])


def load_results(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}

    by_run_id: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"Warning: skipped invalid JSONL line {line_number}: {exc}", file=sys.stderr)
            continue
        run_id = row.get("run_id") or row.get("id")
        if run_id:
            by_run_id[str(run_id)] = row
    return by_run_id


def comparable_runs(
    registry_runs: list[dict[str, Any]], results_by_run: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for run in registry_runs:
        row = dict(run)
        run_id = row.get("run_id")
        if run_id and str(run_id) in results_by_run:
            row.update({k: v for k, v in results_by_run[str(run_id)].items() if v is not None})
        status = str(row.get("status", "")).lower()
        decision = str(row.get("decision", "")).lower()
        run_type = str(row.get("run_type", "")).lower()
        if run_type in {"screening", "smoke"}:
            continue
        if status in {"done", "completed", "accepted"} or decision == "accepted":
            merged.append(row)
    return merged


def group_key(run: dict[str, Any]) -> str:
    dataset = run.get("dataset") or "unknown_dataset"
    split = run.get("split") or run.get("data_split") or "unknown_split"
    return f"{dataset}::{split}"


def check_groups(runs: list[dict[str, Any]]) -> tuple[list[dict[str, str]], int]:
    rows: list[dict[str, str]] = []
    failures = 0
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        groups[group_key(run)].append(run)

    for group, group_runs in sorted(groups.items()):
        for field in HARD_FIELDS:
            observed: dict[str, list[str]] = defaultdict(list)
            missing: list[str] = []
            for run in group_runs:
                run_id = str(run.get("run_id", "<missing-run-id>"))
                value = run.get(field)
                if value is None and field == "split":
                    value = run.get("data_split")
                if value is None:
                    missing.append(run_id)
                else:
                    observed[str(value)].append(run_id)

            if len(observed) <= 1 and not missing:
                status = "PASS"
                expected = next(iter(observed.keys()), "")
                notes = ""
            else:
                status = "FAIL"
                failures += 1
                expected = next(iter(observed.keys()), "")
                notes = "missing: " + ", ".join(missing) if missing else ""

            rows.append(
                {
                    "group": group,
                    "field": field,
                    "expected": expected,
                    "observed": "; ".join(
                        f"{value}: {', '.join(ids)}" for value, ids in sorted(observed.items())
                    ),
                    "status": status,
                    "notes": notes,
                }
            )

    return rows, failures


def render_report(
    registry: Path,
    results: Path | None,
    runs: list[dict[str, Any]],
    rows: list[dict[str, str]],
    failures: int,
) -> str:
    methods = sorted({str(run.get("method_version", "")) for run in runs if run.get("method_version")})
    status = "PASS" if failures == 0 else "FAIL"
    lines = [
        "# Experiment Consistency Report",
        "",
        f"- Overall status: {status}",
        f"- Registry: `{registry}`",
        f"- Results JSONL: `{results}`" if results else "- Results JSONL: not provided",
        f"- Comparable full/accepted runs: {len(runs)}",
        f"- Method versions found: {', '.join(methods) if methods else 'none'}",
        f"- Hard failures: {failures}",
        "",
        "## Required Checks",
        "",
        "| group | field | expected | observed | status | notes |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {group} | {field} | {expected} | {observed} | {status} | {notes} |".format(
                **{k: str(v).replace("|", "\\|") for k, v in row.items()}
            )
        )

    if not runs:
        lines.extend(
            [
                "",
                "## Notes",
                "",
                "No completed full runs were found. This is acceptable before final experiments, "
                "but paper tables must not be written until comparable runs exist.",
            ]
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--results", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    registry_runs = load_registry(args.registry)
    results_by_run = load_results(args.results)
    runs = comparable_runs(registry_runs, results_by_run)
    rows, failures = check_groups(runs)
    report = render_report(args.registry, args.results, runs, rows, failures)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
