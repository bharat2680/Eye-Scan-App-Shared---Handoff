#!/usr/bin/env python3
"""Build a raw candidate manifest for fundus separation review.

This helper creates review-queue rows only. It does not train, does not read or
write model files, and does not move, copy, delete, or alter image files.

Every generated row intentionally has:
- final_label empty
- split = unset
- review_status = unreviewed
- challenge_only = false
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


MANIFEST_COLUMNS = [
    "image_path",
    "source_dataset",
    "source_label",
    "proposed_label",
    "final_label",
    "split",
    "review_status",
    "reviewer",
    "review_notes",
    "lesion_pattern_notes",
    "quality_notes",
    "duplicate_group_id",
    "challenge_only",
    "exclude_reason",
]

APPROVED_LABELS = {
    "normal_or_non_specific",
    "dr_pattern_dominant",
    "hemorrhage_pattern_dominant_non_dr",
    "exudate_macular_pattern_dominant",
    "mixed_hemorrhage_exudate_pattern",
}

SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
}

RESERVED_MANIFEST_OUTPUT_NAMES = {
    "reviewed_manifest_v1.csv",
    "fitting_manifest_v1.csv",
    "challenge_manifest_v1.csv",
}

REFUSED_OUTPUT_NAMES = {
    "model.tflite",
    "labels.txt",
    "fundus_broad_abnormality_v1_efficientnetb0_colab_package.zip",
    "anterior_boundary_v1_efficientnetb0_colab_package.zip",
}

REFUSED_OUTPUT_SUFFIXES = {
    ".tflite",
    ".keras",
    ".h5",
    ".zip",
}

FIT_SPLITS = {"train", "val", "test"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create raw candidate manifest rows for later image review. "
            "Generated rows are not training-ready."
        )
    )
    parser.add_argument(
        "input_folders",
        nargs="+",
        type=Path,
        help="One or more folders to scan recursively for candidate images.",
    )
    parser.add_argument(
        "--source-dataset",
        required=True,
        help="Source dataset name written to every generated row.",
    )
    parser.add_argument(
        "--source-label",
        default="unknown",
        help="Source label written to every generated row. Default: unknown.",
    )
    parser.add_argument(
        "--proposed-label",
        default="",
        choices=sorted(APPROVED_LABELS),
        help=(
            "Optional five-class proposed_label hint. This is never written to "
            "final_label. Omit this flag to leave proposed_label empty."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("raw_candidate_manifest.csv"),
        help="Output CSV path. Default: raw_candidate_manifest.csv.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting an existing output CSV.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report how many candidate image files would be included without writing CSV.",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def warn(message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr)


def validate_input_folders(input_folders: list[Path]) -> list[Path]:
    resolved_folders = []
    for folder in input_folders:
        if not folder.exists():
            fail(f"Input folder does not exist: {folder}")
        if not folder.is_dir():
            fail(f"Input path is not a folder: {folder}")
        resolved_folders.append(folder.resolve())
    return resolved_folders


def validate_output_path(output_path: Path, overwrite: bool, dry_run: bool) -> Path:
    output_path = output_path.expanduser()
    output_name = output_path.name.lower()
    output_suffix = output_path.suffix.lower()

    if output_name in REFUSED_OUTPUT_NAMES or output_suffix in REFUSED_OUTPUT_SUFFIXES:
        fail(
            "Refusing to write package/model artifact-style output path: "
            f"{output_path}"
        )

    if output_name in RESERVED_MANIFEST_OUTPUT_NAMES:
        warn(
            "Output filename resembles a reviewed/fitting/challenge manifest. "
            "This helper is intended for raw_candidate_manifest.csv only."
        )

    if output_path.exists() and not overwrite and not dry_run:
        fail(f"Output already exists. Pass --overwrite to replace it: {output_path}")

    if output_path.exists() and overwrite and output_path.is_dir():
        fail(f"Output path is a directory, not a CSV file: {output_path}")

    return output_path


def find_candidate_images(input_folders: list[Path]) -> tuple[list[Path], dict[str, int]]:
    discovered: list[Path] = []
    duplicate_counter: Counter[str] = Counter()

    for folder in input_folders:
        for path in folder.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
                continue
            resolved = path.resolve()
            discovered.append(resolved)
            duplicate_counter[str(resolved)] += 1

    unique_paths = sorted({path for path in discovered}, key=lambda item: str(item))
    duplicates = {
        image_path: count
        for image_path, count in sorted(duplicate_counter.items())
        if count > 1
    }
    return unique_paths, duplicates


def build_rows(
    image_paths: list[Path],
    source_dataset: str,
    source_label: str,
    proposed_label: str,
) -> list[dict[str, str]]:
    rows = []
    for image_path in image_paths:
        rows.append(
            {
                "image_path": str(image_path),
                "source_dataset": source_dataset,
                "source_label": source_label,
                "proposed_label": proposed_label,
                "final_label": "",
                "split": "unset",
                "review_status": "unreviewed",
                "reviewer": "",
                "review_notes": "",
                "lesion_pattern_notes": "",
                "quality_notes": "",
                "duplicate_group_id": "",
                "challenge_only": "false",
                "exclude_reason": "",
            }
        )
    return rows


def write_csv(output_path: Path, rows: list[dict[str, str]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, str]], output_path: Path, dry_run: bool) -> None:
    final_label_nonempty = sum(1 for row in rows if row["final_label"].strip())
    accepted_rows = sum(1 for row in rows if row["review_status"] == "accepted")
    train_val_test_rows = sum(1 for row in rows if row["split"] in FIT_SPLITS)

    print(f"dry_run = {str(dry_run).lower()}")
    print(f"total rows = {len(rows)}")
    print(f"output path = {output_path}")
    print(f"final_label_nonempty = {final_label_nonempty}")
    print(f"accepted_rows = {accepted_rows}")
    print(f"train_val_test_rows = {train_val_test_rows}")


def main() -> None:
    args = parse_args()
    input_folders = validate_input_folders(args.input_folders)
    output_path = validate_output_path(args.output, args.overwrite, args.dry_run)

    image_paths, duplicate_paths = find_candidate_images(input_folders)
    if duplicate_paths:
        warn(
            "Duplicate candidate image paths detected across input folders: "
            f"{len(duplicate_paths)} unique duplicate paths."
        )

    rows = build_rows(
        image_paths=image_paths,
        source_dataset=args.source_dataset,
        source_label=args.source_label,
        proposed_label=args.proposed_label,
    )

    if args.dry_run:
        summarize(rows, output_path, dry_run=True)
        return

    write_csv(output_path, rows)
    summarize(rows, output_path, dry_run=False)


if __name__ == "__main__":
    main()
