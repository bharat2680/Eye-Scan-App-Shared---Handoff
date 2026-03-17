from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class FoundationModelSpec:
    model_id: str
    title: str
    relative_path: str
    intended_use: str
    license_note: str
    official_source: str


MODEL_SPECS = [
    FoundationModelSpec(
        model_id="visionfm_external_eye",
        title="VisionFM External Eye",
        relative_path=r"VisionFM\ExternalEye\visionfm_external_eye.pth",
        intended_use="anterior quality gate and surface-positive specialists",
        license_note="research and educational use only",
        official_source="https://github.com/ABILab-CUHK/VisionFM",
    ),
    FoundationModelSpec(
        model_id="visionfm_slit_lamp",
        title="VisionFM Slit Lamp",
        relative_path=r"VisionFM\SlitLamp\visionfm_slit_lamp.pth",
        intended_use="cataract and surface-specialist comparison backbone",
        license_note="research and educational use only",
        official_source="https://github.com/ABILab-CUHK/VisionFM",
    ),
    FoundationModelSpec(
        model_id="retfound_dinov2_meh",
        title="RETFound_dinov2_meh",
        relative_path=r"RETFound\Fundus\retfound_dinov2_meh.pth",
        intended_use="fundus DR and glaucoma transfer-learning backbone",
        license_note="non-commercial official release",
        official_source="https://github.com/rmaphoh/RETFound",
    ),
    FoundationModelSpec(
        model_id="visionfm_fundus",
        title="VisionFM Fundus",
        relative_path=r"VisionFM\Fundus\visionfm_fundus.pth",
        intended_use="secondary official fundus backbone",
        license_note="research and educational use only",
        official_source="https://github.com/ABILab-CUHK/VisionFM",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether the expected EyeScan foundation-model files are staged."
    )
    parser.add_argument(
        "--root",
        default=r"F:\datasets\FoundationModels",
        help="Root folder that should contain the staged foundation-model files.",
    )
    parser.add_argument(
        "--output",
        default="datasets/manifests/foundation_model_staging_status.json",
        help="Optional JSON report path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root)
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path(__file__).resolve().parents[1] / output_path

    results = []
    staged_count = 0

    for spec in MODEL_SPECS:
        absolute_path = root / Path(spec.relative_path)
        exists = absolute_path.exists()
        if exists:
            staged_count += 1
        results.append(
            {
                **asdict(spec),
                "expected_path": str(absolute_path),
                "exists": exists,
                "size_bytes": absolute_path.stat().st_size if exists else None,
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            {
                "root": str(root),
                "staged_count": staged_count,
                "total_count": len(MODEL_SPECS),
                "models": results,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Foundation-model staging check: {staged_count}/{len(MODEL_SPECS)} present")
    for result in results:
        status = "present" if result["exists"] else "missing"
        print(f"- {result['model_id']}: {status} :: {result['expected_path']}")
    print(f"JSON report: {output_path}")


if __name__ == "__main__":
    main()
