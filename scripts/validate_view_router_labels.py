#!/usr/bin/env python3
"""Validate reviewed anterior view-router labels before training."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ALLOWED_LABELS = {"iris_visible", "eyelid_dominant", "unclear"}
DEFAULT_INPUT = (
    Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
    / "datasets/anterior/view_router/labels_reviewed_final.csv"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", type=Path, default=DEFAULT_INPUT)
    parser.add_argument(
        "--require-no-pending",
        action="store_true",
        help="Exit non-zero if any rows still have blank/pending review_status.",
    )
    parser.add_argument(
        "--min-included-per-label",
        type=int,
        default=0,
        help="Optional floor for included examples per label.",
    )
    return parser.parse_args()


def parse_bool(value: str) -> str:
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return "1"
    if normalized in {"0", "false", "no", "n"}:
        return "0"
    return ""


def main() -> None:
    args = parse_args()
    rows = list(csv.DictReader(args.input_csv.open("r", encoding="utf-8", newline="")))
    required = {
        "relative_path",
        "source_class",
        "router_label",
        "include_in_router",
        "review_status",
    }
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise SystemExit(f"Missing required CSV columns: {sorted(missing)}")

    label_counts = Counter()
    include_counts = Counter()
    included_label_counts = Counter()
    status_counts = Counter()
    included_by_source = defaultdict(Counter)
    errors: list[str] = []

    for row in rows:
        relative_path = (row.get("relative_path") or "").strip()
        label = (row.get("router_label") or "").strip()
        include = parse_bool(row.get("include_in_router") or "")
        status = (row.get("review_status") or "").strip() or "pending"
        source_class = (row.get("source_class") or "").strip()

        if label not in ALLOWED_LABELS:
            errors.append(f"{relative_path}: invalid router_label={label!r}")
            continue
        if include not in {"0", "1"}:
            errors.append(f"{relative_path}: invalid include_in_router={include!r}")
            continue

        label_counts[label] += 1
        include_counts[include] += 1
        status_counts[status] += 1
        if include == "1":
            included_label_counts[label] += 1
            included_by_source[source_class][label] += 1

    if args.min_included_per_label:
        for label in sorted(ALLOWED_LABELS):
            if included_label_counts.get(label, 0) < args.min_included_per_label:
                errors.append(
                    f"included count for {label!r} is below minimum "
                    f"({included_label_counts.get(label, 0)} < {args.min_included_per_label})"
                )

    if args.require_no_pending and status_counts.get("pending", 0):
        errors.append(f"pending review rows remain: {status_counts['pending']}")

    result = {
        "input_csv": str(args.input_csv),
        "total_rows": len(rows),
        "label_counts": dict(sorted(label_counts.items())),
        "include_counts": {
            "include": include_counts.get("1", 0),
            "hold": include_counts.get("0", 0),
        },
        "included_label_counts": dict(sorted(included_label_counts.items())),
        "review_status_counts": dict(sorted(status_counts.items())),
        "included_by_source": {
            source_class: dict(sorted(counter.items()))
            for source_class, counter in sorted(included_by_source.items())
        },
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
