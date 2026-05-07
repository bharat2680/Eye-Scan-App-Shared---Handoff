#!/usr/bin/env python3
"""Audit-only path resolution checks for fitting_manifest_v1.csv."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    lane_root = script_path.parents[3]
    parser = argparse.ArgumentParser(
        description="Audit fitting manifest image path resolvability without loading images."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=lane_root / "review_manifests" / "fitting_manifest_v1.csv",
        help="Path to fitting_manifest_v1.csv",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=script_path.parents[5],
        help="Repo root used for repo-relative path checks.",
    )
    parser.add_argument(
        "--external-root",
        type=Path,
        default=Path("/Users/bharatsharma/Documents/EyeScan_Local_Data/large_dr_82gb_work"),
        help="External data root to probe for archive-member mappings.",
    )
    return parser.parse_args()


def classify_path(image_path: str) -> str:
    if not image_path:
        return "empty"
    if image_path.startswith(("train/", "test/")):
        return "archive_member_like"
    if image_path.startswith("/"):
        return "absolute_posix"
    if len(image_path) > 2 and image_path[1] == ":" and image_path[2] in ("\\", "/"):
        return "windows_absolute"
    return "other_relative"


def resolve_path(image_path: str, repo_root: Path, external_root: Path) -> Path | None:
    if not image_path:
        return None

    raw_path = Path(image_path)
    if raw_path.exists():
        return raw_path

    repo_candidate = repo_root / image_path
    if repo_candidate.exists():
        return repo_candidate

    if image_path.startswith(("train/", "test/")):
        leaf = Path(image_path).name
        candidates = [
            external_root / image_path,
            external_root / leaf,
            external_root / "images" / leaf,
            external_root / "large_dr_batch_001_moderate_full_review" / "images" / leaf,
            external_root / "tiny_preview_extract" / image_path,
            external_root / "tiny_preview_extract" / leaf,
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate

    return None


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest
    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")

    with manifest_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    paths = [(row.get("image_path") or "").strip() for row in rows]
    pattern_counts = Counter(classify_path(path) for path in paths)
    unique_paths = len(set(paths))
    missing_paths = sum(1 for path in paths if not path)

    resolvable = 0
    unresolved = 0
    resolved_examples: list[str] = []
    unresolved_examples: list[str] = []
    for path in paths:
        resolved = resolve_path(path, args.repo_root, args.external_root)
        if resolved is not None:
            resolvable += 1
            if len(resolved_examples) < 5:
                resolved_examples.append(f"{path} -> {resolved}")
        else:
            unresolved += 1
            if len(unresolved_examples) < 5:
                unresolved_examples.append(path)

    print(f"rows: {len(rows)}")
    print(f"unique_image_path: {unique_paths}")
    print(f"missing_image_path: {missing_paths}")
    print(f"pattern_counts: {dict(pattern_counts)}")
    print(f"resolvable_now: {resolvable}")
    print(f"unresolved_now: {unresolved}")
    print("resolved_examples:")
    for example in resolved_examples:
        print(f"  {example}")
    print("unresolved_examples:")
    for example in unresolved_examples:
        print(f"  {example}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
