#!/usr/bin/env python3
"""Find duplicate and near-duplicate review groups for the anterior view router."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

DEFAULT_DATASET_ROOT = Path(
    "/Users/bharatsharma/Desktop/Image Dataset on Eye Diseases Classification "
    "(Uveitis, Conjunctivitis, Cataract, Eyelid) with Symptoms and SMOTE Validation"
)
DEFAULT_LABEL_CSV = (
    Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
    / "datasets/anterior/view_router/labels_seeded_first_pass.csv"
)
DEFAULT_OUTPUT_CSV = (
    Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
    / "datasets/anterior/view_router/labels_seeded_review_groups.csv"
)
DEFAULT_SUMMARY_JSON = (
    Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
    / "datasets/anterior/view_router/labels_seeded_review_groups_summary.json"
)

BATCH_ORDER = {
    "eyelid_dominant_first": 0,
    "unclear_second": 1,
    "iris_visible_high_risk_next": 2,
    "iris_visible_spotcheck_last": 3,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-root", type=Path, default=DEFAULT_DATASET_ROOT)
    parser.add_argument("--label-csv", type=Path, default=DEFAULT_LABEL_CSV)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY_JSON)
    return parser.parse_args()


def file_sha1(path: Path) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def average_hash(path: Path, size: int = 16) -> str:
    with Image.open(path) as image:
        pixels = list(image.convert("L").resize((size, size)).tobytes())
    average = sum(pixels) / len(pixels)
    bits = "".join("1" if value >= average else "0" for value in pixels)
    return f"{int(bits, 2):0{size * size // 4}x}"


def load_label_rows(path: Path) -> list[dict]:
    rows = list(csv.DictReader(path.open("r", encoding="utf-8", newline="")))
    required = {
        "relative_path",
        "source_class",
        "router_label",
        "suggested_review_batch",
        "review_priority",
        "ambiguity_flags",
    }
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise SystemExit(f"Missing required label CSV columns: {sorted(missing)}")
    return rows


def build_groups(
    dataset_root: Path, label_csv_path: Path, output_csv_path: Path, label_rows: list[dict]
) -> tuple[list[dict], dict]:
    exact_groups: dict[str, list[dict]] = defaultdict(list)
    ahash_groups: dict[tuple[str, str], list[dict]] = defaultdict(list)

    for row in label_rows:
        relative_path = (row.get("relative_path") or "").strip()
        image_path = dataset_root / relative_path
        if not image_path.exists():
            continue

        sha1 = file_sha1(image_path)
        ahash = average_hash(image_path)

        record = {
            "relative_path": relative_path,
            "source_class": (row.get("source_class") or "").strip(),
            "router_label": (row.get("router_label") or "").strip(),
            "suggested_review_batch": (row.get("suggested_review_batch") or "").strip(),
            "review_priority": (row.get("review_priority") or "").strip(),
            "ambiguity_flags": (row.get("ambiguity_flags") or "").strip(),
            "sha1": sha1,
            "ahash": ahash,
        }
        exact_groups[sha1].append(record)
        ahash_groups[(record["source_class"], ahash)].append(record)

    grouped_rows: list[dict] = []
    exact_group_count = 0
    exact_file_count = 0
    near_group_count = 0
    near_file_count = 0

    for sha1, members in sorted(exact_groups.items()):
        if len(members) < 2:
            continue
        exact_group_count += 1
        exact_file_count += len(members)
        group_id = f"exact-{exact_group_count:04d}"
        for member in sorted(members, key=lambda row: row["relative_path"]):
            grouped_rows.append(
                {
                    "group_id": group_id,
                    "group_type": "exact_duplicate",
                    "group_size": len(members),
                    "source_class": member["source_class"],
                    "router_label": member["router_label"],
                    "suggested_review_batch": member["suggested_review_batch"],
                    "review_priority": member["review_priority"],
                    "relative_path": member["relative_path"],
                    "reference_relative_path": sorted(
                        row["relative_path"] for row in members
                    )[0],
                    "group_key": sha1,
                    "review_together_reason": "Exact duplicate file content (same SHA1).",
                    "ambiguity_flags": member["ambiguity_flags"],
                }
            )

    exact_member_paths = {
        row["relative_path"] for row in grouped_rows if row["group_type"] == "exact_duplicate"
    }
    for (source_class, ahash), members in sorted(ahash_groups.items()):
        filtered_members = [
            member for member in members if member["relative_path"] not in exact_member_paths
        ]
        if len(filtered_members) < 2:
            continue
        near_group_count += 1
        near_file_count += len(filtered_members)
        group_id = f"near-{near_group_count:04d}"
        sorted_paths = sorted(row["relative_path"] for row in filtered_members)
        for member in sorted(filtered_members, key=lambda row: row["relative_path"]):
            grouped_rows.append(
                {
                    "group_id": group_id,
                    "group_type": "near_duplicate_candidate",
                    "group_size": len(filtered_members),
                    "source_class": source_class,
                    "router_label": member["router_label"],
                    "suggested_review_batch": member["suggested_review_batch"],
                    "review_priority": member["review_priority"],
                    "relative_path": member["relative_path"],
                    "reference_relative_path": sorted_paths[0],
                    "group_key": ahash,
                    "review_together_reason": (
                        "Near-duplicate candidate within the same source folder "
                        "(matching average hash)."
                    ),
                    "ambiguity_flags": member["ambiguity_flags"],
                }
            )

    grouped_rows.sort(
        key=lambda row: (
            BATCH_ORDER.get(row["suggested_review_batch"], 9),
            row["group_type"] != "exact_duplicate",
            -int(row["group_size"]),
            row["source_class"],
            row["group_id"],
            row["relative_path"],
        )
    )

    summary = {
        "dataset_root": str(dataset_root),
        "label_csv": str(label_csv_path),
        "output_csv": str(output_csv_path),
        "exact_duplicate_groups": exact_group_count,
        "exact_duplicate_files": exact_file_count,
        "near_duplicate_candidate_groups": near_group_count,
        "near_duplicate_candidate_files": near_file_count,
        "group_type_counts": dict(
            sorted(Counter(row["group_type"] for row in grouped_rows).items())
        ),
        "batch_counts": dict(
            sorted(Counter(row["suggested_review_batch"] for row in grouped_rows).items())
        ),
        "source_class_counts": dict(
            sorted(Counter(row["source_class"] for row in grouped_rows).items())
        ),
        "top_groups": [
            {
                "group_id": row["group_id"],
                "group_type": row["group_type"],
                "group_size": row["group_size"],
                "source_class": row["source_class"],
                "suggested_review_batch": row["suggested_review_batch"],
                "paths": [
                    candidate["relative_path"]
                    for candidate in grouped_rows
                    if candidate["group_id"] == row["group_id"]
                ],
            }
            for row in grouped_rows
            if row["relative_path"] == row["reference_relative_path"]
        ][:20],
    }
    return grouped_rows, summary


def write_csv(output_path: Path, rows: list[dict]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "group_id",
        "group_type",
        "group_size",
        "source_class",
        "router_label",
        "suggested_review_batch",
        "review_priority",
        "relative_path",
        "reference_relative_path",
        "group_key",
        "review_together_reason",
        "ambiguity_flags",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    args = parse_args()
    label_rows = load_label_rows(args.label_csv)
    grouped_rows, summary = build_groups(
        args.dataset_root, args.label_csv, args.output_csv, label_rows
    )
    write_csv(args.output_csv, grouped_rows)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
