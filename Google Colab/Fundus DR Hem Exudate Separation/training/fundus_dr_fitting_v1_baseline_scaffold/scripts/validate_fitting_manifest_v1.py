#!/usr/bin/env python3
"""Validation-only checks for Fundus DR fitting_manifest_v1.csv."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


EXPECTED_ROW_COUNT = 1864
EXPECTED_CLASS_COUNTS = {
    "normal_or_non_specific": 466,
    "dr_pattern_dominant": 466,
    "exudate_macular_pattern_dominant": 466,
    "mixed_hemorrhage_exudate_pattern": 466,
}
EXPECTED_SPLIT_COUNTS = {"train": 1304, "val": 280, "test": 280}
REQUIRED_COLUMNS = {
    "evidence_id",
    "source_batch",
    "source_row_id",
    "id_code",
    "image_path",
    "review_bucket",
    "review_status",
    "fitting_split",
}
EXCLUDED_BUCKETS = {
    "hemorrhage_pattern_dominant_non_dr",
    "unusable_low_quality",
    "needs_second_review",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the canonical Fundus DR fitting manifest."
    )
    default_path = (
        Path(__file__).resolve().parents[3]
        / "review_manifests"
        / "fitting_manifest_v1.csv"
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=default_path,
        help="Path to fitting_manifest_v1.csv",
    )
    return parser.parse_args()


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest
    if not manifest_path.exists():
        return fail(f"manifest not found: {manifest_path}")

    with manifest_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        rows = list(reader)

    missing_columns = sorted(REQUIRED_COLUMNS - columns)
    if missing_columns:
        return fail(f"missing required columns: {', '.join(missing_columns)}")

    if len(rows) != EXPECTED_ROW_COUNT:
        return fail(
            f"row count mismatch: expected {EXPECTED_ROW_COUNT}, got {len(rows)}"
        )

    class_counts = Counter(row["review_bucket"] for row in rows)
    if dict(class_counts) != EXPECTED_CLASS_COUNTS:
        return fail(
            f"class counts mismatch: expected {EXPECTED_CLASS_COUNTS}, got {dict(class_counts)}"
        )

    split_counts = Counter(row["fitting_split"] for row in rows)
    if dict(split_counts) != EXPECTED_SPLIT_COUNTS:
        return fail(
            f"split counts mismatch: expected {EXPECTED_SPLIT_COUNTS}, got {dict(split_counts)}"
        )

    duplicate_evidence_id = len(rows) - len({row["evidence_id"] for row in rows})
    if duplicate_evidence_id:
        return fail(f"duplicate evidence_id count: {duplicate_evidence_id}")

    excluded_found = sorted(
        {row["review_bucket"] for row in rows if row["review_bucket"] in EXCLUDED_BUCKETS}
    )
    if excluded_found:
        return fail(f"excluded buckets found: {', '.join(excluded_found)}")

    nonaccepted = sum(1 for row in rows if row["review_status"] != "accepted")
    if nonaccepted:
        return fail(f"non-accepted rows found: {nonaccepted}")

    print("fitting_manifest_v1.csv validation passed")
    print(f"rows: {len(rows)}")
    print(f"class_counts: {dict(class_counts)}")
    print(f"split_counts: {dict(split_counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
