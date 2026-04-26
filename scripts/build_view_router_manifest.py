import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build a JSONL manifest for the anterior view router from a labeling CSV."
    )
    parser.add_argument("--spec", type=Path, required=True, help="Path to dataset spec JSON.")
    parser.add_argument(
        "--label-csv",
        type=Path,
        default=None,
        help="Optional reviewed labeling CSV override. Defaults to label_csv from the spec.",
    )
    return parser.parse_args()


def load_spec(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    spec["spec_path"] = str(path)
    return spec


def deterministic_split_key(value: str) -> int:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()
    return int(digest, 16) % 100


def assign_split(relative_path: str, train_pct: int, val_pct: int) -> str:
    bucket = deterministic_split_key(relative_path)
    if bucket < train_pct:
        return "train"
    if bucket < train_pct + val_pct:
        return "val"
    return "test"


def parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def build_manifest(spec: dict, label_csv_override: Path | None = None) -> tuple[list[dict], dict]:
    dataset_root = Path(spec["dataset_root"]).expanduser()
    label_csv = (
        label_csv_override.expanduser()
        if label_csv_override is not None
        else Path(spec["label_csv"]).expanduser()
    )
    allowed_labels = set(spec["allowed_labels"])
    excluded_prefixes = tuple(spec.get("exclude_filename_prefixes", []))
    train_pct = int(spec.get("train_percent", 70))
    val_pct = int(spec.get("val_percent", 15))

    if not dataset_root.exists():
        raise SystemExit(f"Dataset root not found: {dataset_root}")
    if not label_csv.exists():
        raise SystemExit(f"Label CSV not found: {label_csv}")

    rows = []
    split_counts = defaultdict(Counter)
    label_counts = Counter()
    skipped_counts = Counter()

    with label_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"relative_path", "source_class", "router_label", "include_in_router"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Missing required CSV columns: {sorted(missing)}")

        for row in reader:
            relative_path = (row.get("relative_path") or "").strip()
            source_class = (row.get("source_class") or "").strip()
            router_label = (row.get("router_label") or "").strip()
            include = parse_bool(row.get("include_in_router") or "")

            if not relative_path:
                skipped_counts["blank_relative_path"] += 1
                continue

            image_path = dataset_root / relative_path
            if not image_path.exists():
                skipped_counts["missing_file"] += 1
                continue

            if image_path.suffix.lower() not in IMAGE_SUFFIXES:
                skipped_counts["unsupported_suffix"] += 1
                continue

            if image_path.name.lower().startswith(excluded_prefixes):
                skipped_counts["excluded_augmented_prefix"] += 1
                continue

            if not include:
                skipped_counts["manual_exclude"] += 1
                continue

            if router_label not in allowed_labels:
                skipped_counts["invalid_router_label"] += 1
                continue

            split = assign_split(relative_path, train_pct=train_pct, val_pct=val_pct)
            record = {
                "path": str(image_path),
                "relative_path": relative_path,
                "source_class": source_class,
                "router_label": router_label,
                "split": split,
            }
            rows.append(record)
            split_counts[split][router_label] += 1
            label_counts[router_label] += 1

    summary = {
        "included_total": len(rows),
        "label_counts": dict(label_counts),
        "split_counts": {split: dict(counter) for split, counter in split_counts.items()},
        "skipped_counts": dict(skipped_counts),
    }
    return rows, summary


def write_manifest(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def main():
    args = parse_args()
    spec = load_spec(args.spec)
    rows, summary = build_manifest(spec, label_csv_override=args.label_csv)
    output_manifest = Path(spec["output_manifest"]).expanduser()
    write_manifest(output_manifest, rows)

    print(json.dumps(
        {
            "dataset_name": spec["dataset_name"],
            "label_csv": str((args.label_csv or Path(spec["label_csv"])).expanduser()),
            "output_manifest": str(output_manifest),
            **summary,
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
