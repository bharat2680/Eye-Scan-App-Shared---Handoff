#!/usr/bin/env python3
"""Resolve fitting_manifest_v1.csv rows to Dell/Windows external cache paths."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


EXPECTED_TOTAL_ROWS = 1864
EXPECTED_LARGE_DR_ROWS = 1766
EXPECTED_BATCH_008_ROWS = 98
REQUIRED_MANIFEST_COLUMNS = {
    "evidence_id",
    "image_path",
    "review_bucket",
    "fitting_split",
}
REQUIRED_AUDIT_COLUMNS = {
    "evidence_id",
    "image_path",
    "cached_external_path",
    "cache_exists",
}


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    lane_root = script_path.parents[3]
    scaffold_root = script_path.parents[1]
    parser = argparse.ArgumentParser(
        description=(
            "Resolve fitting_manifest_v1.csv rows to Dell/Windows external cache "
            "paths without copying images."
        )
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=lane_root / "review_manifests" / "fitting_manifest_v1.csv",
        help="Path to fitting_manifest_v1.csv",
    )
    parser.add_argument(
        "--large-dr-audit",
        type=Path,
        default=(
            scaffold_root
            / "data_cache_audit"
            / "fitting_v1_image_cache_manifest_windows.csv"
        ),
        help="Path to the Large DR Windows cache audit CSV",
    )
    parser.add_argument(
        "--batch-008-audit",
        type=Path,
        default=(
            scaffold_root
            / "data_cache_audit"
            / "batch_008_fitting_image_cache_manifest_windows.csv"
        ),
        help="Path to the Batch 008 Windows cache audit CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            r"F:\EyeScan_Local_Data\large_dr_82gb_work\fitting_v1_resolved_manifest_windows.csv"
        ),
        help="Local-only output CSV path written outside the repo by default",
    )
    return parser.parse_args()


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def load_csv_rows(path: Path, required_columns: set[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(required_columns - columns)
        if missing:
            raise ValueError(f"{path} missing required columns: {', '.join(missing)}")
        return list(reader)


def build_audit_index(
    rows: list[dict[str, str]], label: str
) -> dict[tuple[str, str], dict[str, str]]:
    index: dict[tuple[str, str], dict[str, str]] = {}
    duplicates: list[str] = []
    for row in rows:
        key = (row["evidence_id"], row["image_path"])
        if key in index:
            duplicates.append(f"{label}:{row['evidence_id']}:{row['image_path']}")
        index[key] = row
    if duplicates:
        raise ValueError(f"duplicate audit keys found: {duplicates[:5]}")
    return index


def resolve_row(
    row: dict[str, str],
    large_dr_index: dict[tuple[str, str], dict[str, str]],
    batch_008_index: dict[tuple[str, str], dict[str, str]],
) -> tuple[dict[str, str], str]:
    image_path = row["image_path"]
    evidence_id = row["evidence_id"]
    key = (evidence_id, image_path)
    source = "large_dr" if image_path.startswith("train/") else "batch_008"
    audit_row = (
        large_dr_index.get(key) if source == "large_dr" else batch_008_index.get(key)
    )
    if audit_row is None:
        raise KeyError(f"missing audit mapping for {evidence_id} -> {image_path}")

    cached_external_path = (audit_row.get("cached_external_path") or "").strip()
    cache_exists = (audit_row.get("cache_exists") or "").strip().lower()
    if not cached_external_path:
        raise ValueError(f"empty cached_external_path for {evidence_id} -> {image_path}")
    if cache_exists != "true":
        raise ValueError(f"audit says cache missing for {evidence_id} -> {image_path}")

    resolved_path = Path(cached_external_path)
    if not resolved_path.exists():
        raise FileNotFoundError(
            f"resolved cache file not found for {evidence_id}: {resolved_path}"
        )

    resolved = dict(row)
    resolved["resolved_external_path"] = str(resolved_path)
    resolved["resolution_source"] = source
    resolved["resolved_file_size_bytes"] = str(resolved_path.stat().st_size)
    return resolved, source


def main() -> int:
    args = parse_args()
    try:
        manifest_rows = load_csv_rows(args.manifest, REQUIRED_MANIFEST_COLUMNS)
        large_dr_audit_rows = load_csv_rows(args.large_dr_audit, REQUIRED_AUDIT_COLUMNS)
        batch_008_audit_rows = load_csv_rows(
            args.batch_008_audit, REQUIRED_AUDIT_COLUMNS
        )
    except FileNotFoundError as exc:
        return fail(f"required file not found: {exc}")
    except ValueError as exc:
        return fail(str(exc))

    if len(manifest_rows) != EXPECTED_TOTAL_ROWS:
        return fail(
            f"fitting manifest row count mismatch: expected {EXPECTED_TOTAL_ROWS}, "
            f"got {len(manifest_rows)}"
        )

    large_dr_index = build_audit_index(large_dr_audit_rows, "large_dr")
    batch_008_index = build_audit_index(batch_008_audit_rows, "batch_008")

    resolved_rows: list[dict[str, str]] = []
    resolved_counts: Counter[str] = Counter()
    unresolved_errors: list[str] = []
    for row in manifest_rows:
        try:
            resolved_row, source = resolve_row(row, large_dr_index, batch_008_index)
        except (FileNotFoundError, KeyError, ValueError) as exc:
            unresolved_errors.append(str(exc))
            continue
        resolved_rows.append(resolved_row)
        resolved_counts[source] += 1

    if unresolved_errors:
        preview = "\n".join(unresolved_errors[:10])
        return fail(
            "failed to resolve all rows. First errors:\n"
            f"{preview}\n"
            f"unresolved_count={len(unresolved_errors)}"
        )

    total_resolved = len(resolved_rows)
    large_dr_resolved = resolved_counts["large_dr"]
    batch_008_resolved = resolved_counts["batch_008"]
    if total_resolved != EXPECTED_TOTAL_ROWS:
        return fail(
            f"total resolved mismatch: expected {EXPECTED_TOTAL_ROWS}, got {total_resolved}"
        )
    if large_dr_resolved != EXPECTED_LARGE_DR_ROWS:
        return fail(
            f"Large DR resolved mismatch: expected {EXPECTED_LARGE_DR_ROWS}, "
            f"got {large_dr_resolved}"
        )
    if batch_008_resolved != EXPECTED_BATCH_008_ROWS:
        return fail(
            f"Batch 008 resolved mismatch: expected {EXPECTED_BATCH_008_ROWS}, "
            f"got {batch_008_resolved}"
        )

    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(manifest_rows[0].keys()) + [
        "resolved_external_path",
        "resolution_source",
        "resolved_file_size_bytes",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resolved_rows)

    print("Windows fitting image resolution passed")
    print(f"manifest: {args.manifest}")
    print(f"large_dr_audit: {args.large_dr_audit}")
    print(f"batch_008_audit: {args.batch_008_audit}")
    print(f"resolved_total: {total_resolved}")
    print(f"resolved_large_dr: {large_dr_resolved}")
    print(f"resolved_batch_008: {batch_008_resolved}")
    print(f"output_manifest: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
