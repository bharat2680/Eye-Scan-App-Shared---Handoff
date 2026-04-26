#!/usr/bin/env python3
"""Export pre-filtered anterior view router review CSV batches."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
DEFAULT_INPUT = ROOT / "datasets/anterior/view_router/labels_seeded_first_pass.csv"
DEFAULT_GROUPS = ROOT / "datasets/anterior/view_router/labels_seeded_review_groups.csv"
DEFAULT_OUTPUT_DIR = ROOT / "datasets/anterior/view_router/review_batches"

BATCH_ORDER = [
    "eyelid_dominant_first",
    "unclear_second",
    "iris_visible_high_risk_next",
    "iris_visible_spotcheck_last",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--groups-csv", type=Path, default=DEFAULT_GROUPS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--batches",
        nargs="+",
        default=BATCH_ORDER[:3],
        help="Suggested review batches to export in priority order.",
    )
    return parser.parse_args()


def load_group_index(groups_csv: Path) -> dict[str, dict[str, str]]:
    rows = list(csv.DictReader(groups_csv.open("r", encoding="utf-8", newline="")))
    groups_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups_by_id[row["group_id"]].append(row)

    index: dict[str, dict[str, str]] = {}
    for group_id, group_rows in groups_by_id.items():
        peer_paths = [item["relative_path"] for item in group_rows]
        joined_peers = " | ".join(peer_paths)
        for row in group_rows:
            index[row["relative_path"]] = {
                "review_group_id": row["group_id"],
                "review_group_type": row["group_type"],
                "review_group_size": row["group_size"],
                "review_group_reference_relative_path": row["reference_relative_path"],
                "review_group_key": row["group_key"],
                "review_together_reason": row["review_together_reason"],
                "review_group_peer_paths": joined_peers,
            }
    return index


def build_batch_filename(position: int, batch_name: str) -> str:
    return f"labels_review_batch_{position:02d}_{batch_name}.csv"


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    seed_rows = list(csv.DictReader(args.input_csv.open("r", encoding="utf-8", newline="")))
    if not seed_rows:
        raise SystemExit("No seeded rows found.")

    group_index = load_group_index(args.groups_csv)

    base_fieldnames = list(seed_rows[0].keys())
    extra_fieldnames = [
        "review_group_id",
        "review_group_type",
        "review_group_size",
        "review_group_reference_relative_path",
        "review_group_key",
        "review_together_reason",
        "review_group_peer_paths",
    ]
    fieldnames = base_fieldnames + extra_fieldnames

    summary: dict[str, object] = {
        "input_csv": str(args.input_csv),
        "groups_csv": str(args.groups_csv),
        "output_dir": str(args.output_dir),
        "exported_batches": [],
    }

    for position, batch_name in enumerate(args.batches, start=1):
        rows = [row for row in seed_rows if row.get("suggested_review_batch") == batch_name]
        rows.sort(
            key=lambda row: (
                row.get("review_priority") != "high",
                row.get("source_class", ""),
                row.get("relative_path", ""),
            )
        )

        output_csv = args.output_dir / build_batch_filename(position, batch_name)
        label_counts = Counter(row.get("router_label", "") for row in rows)
        include_counts = Counter(row.get("include_in_router", "") for row in rows)
        status_counts = Counter(row.get("review_status", "") for row in rows)
        grouped_rows = 0

        with output_csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                group_meta = group_index.get(
                    row.get("relative_path", ""),
                    {
                        "review_group_id": "",
                        "review_group_type": "",
                        "review_group_size": "",
                        "review_group_reference_relative_path": "",
                        "review_group_key": "",
                        "review_together_reason": "",
                        "review_group_peer_paths": "",
                    },
                )
                if group_meta["review_group_id"]:
                    grouped_rows += 1
                enriched = dict(row)
                enriched.update(group_meta)
                writer.writerow(enriched)

        summary["exported_batches"].append(
            {
                "batch_name": batch_name,
                "output_csv": str(output_csv),
                "row_count": len(rows),
                "grouped_row_count": grouped_rows,
                "label_counts": dict(sorted(label_counts.items())),
                "include_counts": {
                    "include": include_counts.get("1", 0),
                    "hold": include_counts.get("0", 0),
                },
                "review_status_counts": dict(sorted(status_counts.items())),
            }
        )

    summary_path = args.output_dir / "review_batch_export_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
