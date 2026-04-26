from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path


def load_spec(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def bucket_for_name(name: str) -> int:
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()
    return int(digest, 16) % 100


def split_for_path(relative_path: str, train_percent: int, val_percent: int) -> str:
    bucket = bucket_for_name(relative_path)
    if bucket < train_percent:
        return "train"
    if bucket < train_percent + val_percent:
        return "val"
    return "test"


def safe_export_name(relative_path: str) -> str:
    return relative_path.replace("/", "__").replace("\\", "__")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_export(spec: dict) -> dict:
    dataset_root = Path(spec["dataset_root"]).expanduser().resolve()
    label_csv = Path(spec["label_csv"]).expanduser().resolve()
    output_dir = Path(spec["output_dir"]).expanduser().resolve()
    allowed_labels = list(spec["allowed_labels"])
    exclude_prefixes = tuple(spec.get("exclude_filename_prefixes", []))
    train_percent = int(spec["train_percent"])
    val_percent = int(spec["val_percent"])

    if not dataset_root.exists():
        raise FileNotFoundError(f"Dataset root not found: {dataset_root}")
    if not label_csv.exists():
        raise FileNotFoundError(f"Label CSV not found: {label_csv}")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    splits_root = output_dir / "splits"
    metadata_root = output_dir / "metadata"
    metadata_root.mkdir(parents=True, exist_ok=True)

    manifest_path = metadata_root / "anterior_view_router_v1_binary_manifest.jsonl"
    label_map_path = metadata_root / "label_map.json"
    summary_path = metadata_root / "export_summary.json"
    zip_path = output_dir.parent / f"{output_dir.name}.zip"

    label_map = {label: idx for idx, label in enumerate(sorted(allowed_labels))}
    write_json(label_map_path, label_map)

    rows_written = 0
    split_counts: dict[str, Counter] = defaultdict(Counter)
    source_class_counts: dict[str, Counter] = defaultdict(Counter)
    skipped_counts = Counter()

    with label_csv.open("r", encoding="utf-8", newline="") as handle, manifest_path.open(
        "w", encoding="utf-8"
    ) as manifest_handle:
        reader = csv.DictReader(handle)
        for row in reader:
            relative_path = (row.get("relative_path") or "").strip()
            if not relative_path:
                skipped_counts["missing_relative_path"] += 1
                continue

            file_name = Path(relative_path).name
            if exclude_prefixes and file_name.startswith(exclude_prefixes):
                skipped_counts["excluded_prefix"] += 1
                continue

            router_label = (row.get("router_label") or "").strip()
            if router_label not in allowed_labels:
                skipped_counts["filtered_label"] += 1
                continue

            if not truthy(row.get("include_in_router", "0")):
                skipped_counts["excluded_by_review"] += 1
                continue

            source_path = dataset_root / relative_path
            if not source_path.exists():
                skipped_counts["missing_source_file"] += 1
                continue

            split = split_for_path(relative_path, train_percent=train_percent, val_percent=val_percent)
            export_name = safe_export_name(relative_path)
            export_relative_path = Path("splits") / split / router_label / export_name
            export_path = output_dir / export_relative_path
            export_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, export_path)

            payload = {
                "path": export_relative_path.as_posix(),
                "relative_path": relative_path,
                "source_class": row.get("source_class", "").strip(),
                "router_label": router_label,
                "split": split,
            }
            manifest_handle.write(json.dumps(payload) + "\n")

            rows_written += 1
            split_counts[split][router_label] += 1
            source_class_counts[row.get("source_class", "").strip()][router_label] += 1

    if zip_path.exists():
        zip_path.unlink()
    shutil.make_archive(str(output_dir), "zip", root_dir=output_dir.parent, base_dir=output_dir.name)

    summary = {
        "dataset_name": spec["dataset_name"],
        "dataset_root": str(dataset_root),
        "label_csv": str(label_csv),
        "output_dir": str(output_dir),
        "output_zip": str(zip_path),
        "manifest_path": str(manifest_path),
        "label_map_path": str(label_map_path),
        "allowed_labels": allowed_labels,
        "split_policy": {
            "train_percent": train_percent,
            "val_percent": val_percent,
            "test_percent": 100 - train_percent - val_percent,
            "split_key": "sha1(relative_path) % 100",
        },
        "label_map": label_map,
        "included_rows": rows_written,
        "split_counts": {split: dict(counter) for split, counter in split_counts.items()},
        "source_class_counts": {source: dict(counter) for source, counter in source_class_counts.items()},
        "skipped_counts": dict(skipped_counts),
    }
    write_json(summary_path, summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Export the reviewed binary anterior view-router dataset for Colab.")
    parser.add_argument(
        "--spec",
        default="/Users/bharatsharma/Documents/Playground/EyeScan_Shared/configs/anterior_view_router_v1_binary_colab_export_spec.json",
        help="Path to the export spec JSON.",
    )
    args = parser.parse_args()

    spec_path = Path(args.spec).expanduser().resolve()
    summary = build_export(load_spec(spec_path))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
