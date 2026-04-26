#!/usr/bin/env python3
"""Resolve reviewed router labels into a manifest-ready CSV."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


DEFAULT_INPUT = (
    Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
    / "datasets/anterior/view_router/labels_seeded_first_pass.csv"
)
DEFAULT_OUTPUT = (
    Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
    / "datasets/anterior/view_router/labels_reviewed_final.csv"
)
ALLOWED_LABELS = {"iris_visible", "eyelid_dominant", "unclear"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT)
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
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)

    required = {
        "relative_path",
        "source_class",
        "router_label",
        "include_in_router",
        "final_router_label",
        "final_include_in_router",
    }
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise SystemExit(f"Missing required CSV columns: {sorted(missing)}")

    resolved_label_counts = Counter()
    resolved_include_counts = Counter()
    override_counts = Counter()

    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "relative_path",
            "source_class",
            "router_label",
            "include_in_router",
            "seed_router_label",
            "seed_include_in_router",
            "suggested_review_batch",
            "review_status",
            "review_notes",
            "seed_confidence",
            "review_priority",
            "width",
            "height",
            "aspect_ratio",
            "min_dim",
            "ambiguity_flags",
            "heuristic_reason",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            seed_label = (row.get("router_label") or "").strip()
            seed_include = parse_bool(row.get("include_in_router") or "")
            final_label = (row.get("final_router_label") or "").strip()
            final_include = parse_bool(row.get("final_include_in_router") or "")

            resolved_label = final_label or seed_label
            resolved_include = final_include or seed_include

            if resolved_label not in ALLOWED_LABELS:
                raise SystemExit(
                    f"Invalid resolved label for {row.get('relative_path')}: {resolved_label}"
                )
            if resolved_include not in {"0", "1"}:
                raise SystemExit(
                    f"Invalid resolved include flag for {row.get('relative_path')}: {resolved_include}"
                )

            if final_label and final_label != seed_label:
                override_counts["router_label_override"] += 1
            if final_include and final_include != seed_include:
                override_counts["include_override"] += 1

            resolved_label_counts[resolved_label] += 1
            resolved_include_counts[resolved_include] += 1

            writer.writerow(
                {
                    "relative_path": row.get("relative_path", ""),
                    "source_class": row.get("source_class", ""),
                    "router_label": resolved_label,
                    "include_in_router": resolved_include,
                    "seed_router_label": seed_label,
                    "seed_include_in_router": seed_include,
                    "suggested_review_batch": row.get("suggested_review_batch", ""),
                    "review_status": row.get("review_status", ""),
                    "review_notes": row.get("review_notes", ""),
                    "seed_confidence": row.get("seed_confidence", ""),
                    "review_priority": row.get("review_priority", ""),
                    "width": row.get("width", ""),
                    "height": row.get("height", ""),
                    "aspect_ratio": row.get("aspect_ratio", ""),
                    "min_dim": row.get("min_dim", ""),
                    "ambiguity_flags": row.get("ambiguity_flags", ""),
                    "heuristic_reason": row.get("heuristic_reason", ""),
                }
            )

    print(
        json.dumps(
            {
                "input_csv": str(args.input_csv),
                "output_csv": str(args.output_csv),
                "resolved_label_counts": dict(sorted(resolved_label_counts.items())),
                "resolved_include_counts": {
                    "include": resolved_include_counts.get("1", 0),
                    "hold": resolved_include_counts.get("0", 0),
                },
                "overrides_applied": dict(sorted(override_counts.items())),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
