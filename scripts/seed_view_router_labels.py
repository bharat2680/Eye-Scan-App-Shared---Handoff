#!/usr/bin/env python3
"""Generate a heuristic first-pass labeling CSV for the anterior view router.

This script seeds proposed router labels for human review. It does not claim
final labels; instead it emits:

- a proposed router label within the strict label space
- an include_in_router default (0 for low-confidence seeds)
- metadata to make manual review faster
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
ALLOWED_LABELS = {"iris_visible", "eyelid_dominant", "unclear"}
IMAGE_DATASET_NAME = (
    "Image Dataset on Eye Diseases Classification "
    "(Uveitis, Conjunctivitis, Cataract, Eyelid) with Symptoms and SMOTE Validation"
)
DEFAULT_DATASET_ROOT = Path("/Users/bharatsharma/Desktop") / IMAGE_DATASET_NAME
DEFAULT_OUTPUT_CSV = (
    Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
    / "datasets/anterior/view_router/labels_seeded_first_pass.csv"
)
DEFAULT_SUMMARY_JSON = (
    Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
    / "datasets/anterior/view_router/labels_seeded_first_pass_summary.json"
)


@dataclass
class SeedRow:
    relative_path: str
    source_class: str
    router_label: str
    include_in_router: int
    suggested_review_batch: str
    seed_confidence: str
    review_priority: str
    width: int
    height: int
    aspect_ratio: float
    min_dim: int
    ambiguity_flags: str
    heuristic_reason: str


def iter_images(dataset_root: Path) -> Iterable[Path]:
    for source_dir in sorted(path for path in dataset_root.iterdir() if path.is_dir()):
        for image_path in sorted(source_dir.iterdir()):
            if not image_path.is_file():
                continue
            if image_path.name.startswith("."):
                continue
            if image_path.name.startswith("aug_"):
                continue
            if image_path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            yield image_path


def classify_seed(source_class: str, width: int, height: int) -> tuple[str, int, str, str, list[str], str]:
    min_dim = min(width, height)
    aspect_ratio = round(width / height, 4) if height else 0.0

    flags: list[str] = []
    include_in_router = 1
    seed_confidence = "medium"
    review_priority = "medium"

    very_small = min_dim < 80
    small = min_dim < 120
    extreme_aspect = aspect_ratio > 1.9 or aspect_ratio < 0.8
    square = 0.95 <= aspect_ratio <= 1.05

    if very_small:
        flags.append("very_low_resolution")
        include_in_router = 0
        seed_confidence = "low"
        review_priority = "high"
    elif small:
        flags.append("low_resolution")
        seed_confidence = "low"
        review_priority = "high"

    if extreme_aspect:
        flags.append("extreme_aspect")
        include_in_router = 0
        seed_confidence = "low"
        review_priority = "high"

    if source_class == "Eyelid":
        flags.append("eyelid_source_folder")
        review_priority = "high"
        if very_small or extreme_aspect:
            router_label = "unclear"
            seed_confidence = "low"
            include_in_router = 0
            reason = (
                "Seeded unclear because the image comes from the Eyelid folder but "
                "its framing or resolution makes view-type assignment unreliable."
            )
        else:
            router_label = "eyelid_dominant"
            reason = (
                "Seeded eyelid_dominant from the Eyelid source folder. Human review "
                "should rescue any images where the iris is sufficiently visible."
            )
    else:
        router_label = "iris_visible"
        reason = (
            "Seeded iris_visible from a non-Eyelid disease folder because these "
            "sources usually present broader anterior surface views."
        )

        if source_class == "Normal" and square:
            flags.append("square_normal_source")
            if min_dim <= 80:
                flags.append("manual_review_for_router_bias")
                include_in_router = 0
                seed_confidence = "low"
                review_priority = "high"
                reason = (
                    "Seeded iris_visible from the Normal folder, but this image comes "
                    "from the tiny square normal subset and should be manually reviewed "
                    "before being used for router training."
                )
            else:
                review_priority = "medium"

        if source_class in {"Conjunctivitis", "Uveitis", "Pterygium"}:
            review_priority = "medium" if review_priority != "high" else review_priority
            flags.append("disease_folder_surface_view")

        if very_small and source_class != "Eyelid":
            flags.append("size_based_holdout")

    if source_class == "Pterygium":
        flags.append("homogeneous_source_folder")

    return (
        router_label,
        include_in_router,
        seed_confidence,
        review_priority,
        flags,
        reason,
    )


def build_rows(dataset_root: Path) -> list[SeedRow]:
    rows: list[SeedRow] = []
    for image_path in iter_images(dataset_root):
        source_class = image_path.parent.name
        relative_path = image_path.relative_to(dataset_root).as_posix()

        with Image.open(image_path) as image:
            width, height = image.size

        (
            router_label,
            include_in_router,
            seed_confidence,
            review_priority,
            flags,
            heuristic_reason,
        ) = classify_seed(source_class, width, height)

        if router_label not in ALLOWED_LABELS:
            raise ValueError(f"Unexpected router label: {router_label}")

        rows.append(
            SeedRow(
                relative_path=relative_path,
                source_class=source_class,
                router_label=router_label,
                include_in_router=include_in_router,
                suggested_review_batch=suggest_review_batch(
                    router_label=router_label,
                    include_in_router=include_in_router,
                    review_priority=review_priority,
                ),
                seed_confidence=seed_confidence,
                review_priority=review_priority,
                width=width,
                height=height,
                aspect_ratio=round(width / height, 4) if height else 0.0,
                min_dim=min(width, height),
                ambiguity_flags=";".join(flags),
                heuristic_reason=heuristic_reason,
            )
        )
    return rows


def write_csv(rows: list[SeedRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "relative_path",
        "source_class",
        "router_label",
        "include_in_router",
        "suggested_review_batch",
        "final_router_label",
        "final_include_in_router",
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
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_rows = sorted(
        rows,
        key=lambda row: (
            priority_order.get(row.review_priority, 9),
            row.include_in_router,
            row.source_class,
            row.relative_path,
        ),
    )
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted_rows:
            record = {
                **row.__dict__,
                "final_router_label": "",
                "final_include_in_router": "",
                "review_status": "pending",
                "review_notes": "",
            }
            writer.writerow(record)


def build_summary(rows: list[SeedRow], dataset_root: Path, output_csv: Path) -> dict:
    label_counts = Counter(row.router_label for row in rows)
    include_counts = Counter(row.include_in_router for row in rows)
    batch_counts = Counter(row.suggested_review_batch for row in rows)
    priority_counts = Counter(row.review_priority for row in rows)
    confidence_counts = Counter(row.seed_confidence for row in rows)
    source_counts = Counter(row.source_class for row in rows)
    label_by_source = Counter((row.source_class, row.router_label) for row in rows)
    flag_counts = Counter(
        flag
        for row in rows
        for flag in row.ambiguity_flags.split(";")
        if flag
    )

    return {
        "dataset_root": str(dataset_root),
        "output_csv": str(output_csv),
        "total_rows": len(rows),
        "proposed_label_counts": dict(sorted(label_counts.items())),
        "include_in_router_counts": {
            "include": include_counts.get(1, 0),
            "hold_for_review": include_counts.get(0, 0),
        },
        "suggested_review_batch_counts": dict(sorted(batch_counts.items())),
        "review_priority_counts": dict(sorted(priority_counts.items())),
        "seed_confidence_counts": dict(sorted(confidence_counts.items())),
        "source_class_counts": dict(sorted(source_counts.items())),
        "source_by_proposed_label_counts": {
            f"{source_class}:{router_label}": count
            for (source_class, router_label), count in sorted(label_by_source.items())
        },
        "ambiguity_flag_counts": dict(sorted(flag_counts.items())),
        "heuristics": {
            "Eyelid": (
                "Seed eyelid images to eyelid_dominant unless the image is too small "
                "or too extreme in aspect ratio, in which case hold it as unclear."
            ),
            "Normal": (
                "Seed normal images to iris_visible, but hold tiny square examples for "
                "manual review to avoid resolution/source bias in the router."
            ),
            "Conjunctivitis/Uveitis/Pterygium/Cataract": (
                "Seed non-eyelid disease folders to iris_visible by default, while "
                "flagging lower-resolution examples for manual review."
            ),
        },
    }


def suggest_review_batch(router_label: str, include_in_router: int, review_priority: str) -> str:
    if router_label == "eyelid_dominant":
        return "eyelid_dominant_first"
    if router_label == "unclear":
        return "unclear_second"
    if router_label == "iris_visible" and (
        review_priority == "high" or include_in_router == 0
    ):
        return "iris_visible_high_risk_next"
    return "iris_visible_spotcheck_last"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-root", type=Path, default=DEFAULT_DATASET_ROOT)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY_JSON)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_rows(args.dataset_root)
    write_csv(rows, args.output_csv)
    summary = build_summary(rows, args.dataset_root, args.output_csv)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
