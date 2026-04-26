from __future__ import annotations

import argparse
import csv
import json
import mimetypes
import tempfile
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
REVIEW_BATCH_DIR = (
    Path("/Users/bharatsharma/Documents/Playground/EyeScan_Shared")
    / "datasets/anterior/view_router/review_batches"
)
DATASET_ROOT = Path(
    "/Users/bharatsharma/Desktop/Image Dataset on Eye Diseases Classification "
    "(Uveitis, Conjunctivitis, Cataract, Eyelid) with Symptoms and SMOTE Validation"
)
DEFAULT_BATCH = "labels_review_batch_01_eyelid_dominant_first.csv"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8010

ALLOWED_LABELS = {"", "iris_visible", "eyelid_dominant", "unclear"}
ALLOWED_INCLUDE = {"", "0", "1"}
ALLOWED_STATUS = {
    "",
    "pending",
    "confirmed_seed",
    "changed_seed",
    "excluded_from_router",
    "needs_second_pass",
}
EDITABLE_FIELDS = {
    "final_router_label",
    "final_include_in_router",
    "review_status",
    "review_notes",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    return parser.parse_args()


def list_batches() -> list[Path]:
    return sorted(REVIEW_BATCH_DIR.glob("labels_review_batch_*.csv"))


def batch_path_from_name(name: str | None) -> Path:
    if not name:
        name = DEFAULT_BATCH
    candidate = (REVIEW_BATCH_DIR / name).resolve()
    if not candidate.exists() or candidate.suffix.lower() != ".csv":
        raise FileNotFoundError(name)
    if not candidate.is_relative_to(REVIEW_BATCH_DIR.resolve()):
        raise FileNotFoundError(name)
    return candidate


def load_rows(batch_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with batch_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    return rows, fieldnames


def atomic_write_rows(
    batch_path: Path, fieldnames: list[str], rows: list[dict[str, str]]
) -> None:
    batch_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", newline="", delete=False, dir=str(batch_path.parent)
    ) as tmp:
        writer = csv.DictWriter(tmp, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
        temp_name = tmp.name
    Path(temp_name).replace(batch_path)


def current_row_payload(batch_name: str, index: int) -> dict:
    batch_path = batch_path_from_name(batch_name)
    rows, _ = load_rows(batch_path)
    if not rows:
        raise IndexError("No rows found in batch.")
    if index < 0 or index >= len(rows):
        raise IndexError(f"Index out of range: {index}")
    row = dict(rows[index])
    image_path = resolve_image_path(row.get("relative_path", ""))
    row["image_url"] = f"/api/image?batch={batch_name}&index={index}"
    row["image_exists"] = image_path is not None
    return {
        "batch": batch_name,
        "index": index,
        "total_rows": len(rows),
        "row": row,
        "progress": summarize_rows(rows),
    }


def resolve_image_path(relative_path: str) -> Path | None:
    if not relative_path:
        return None
    path = (DATASET_ROOT / relative_path).resolve()
    if not path.exists():
        return None
    if not path.is_relative_to(DATASET_ROOT.resolve()):
        return None
    return path


def summarize_rows(rows: list[dict[str, str]]) -> dict[str, int]:
    total = len(rows)
    pending = 0
    reviewed = 0
    needs_second_pass = 0
    for row in rows:
        status = (row.get("review_status") or "").strip()
        if status == "pending":
            pending += 1
        elif status == "needs_second_pass":
            reviewed += 1
            needs_second_pass += 1
        elif status:
            reviewed += 1
        else:
            pending += 1
    return {
        "total": total,
        "pending": pending,
        "reviewed": reviewed,
        "needs_second_pass": needs_second_pass,
    }


def first_pending_index(rows: list[dict[str, str]]) -> int:
    for idx, row in enumerate(rows):
        status = (row.get("review_status") or "").strip()
        if status in {"", "pending"}:
            return idx
    return 0


class ReviewerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/batches":
            self.handle_batches()
            return
        if parsed.path == "/api/item":
            self.handle_item(parsed)
            return
        if parsed.path == "/api/first-pending":
            self.handle_first_pending(parsed)
            return
        if parsed.path == "/api/image":
            self.handle_image(parsed)
            return
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/save":
            self.handle_save()
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def handle_batches(self) -> None:
        batches = []
        for path in list_batches():
            rows, _ = load_rows(path)
            batches.append(
                {
                    "name": path.name,
                    "label": path.stem,
                    "row_count": len(rows),
                    "progress": summarize_rows(rows),
                }
            )
        self.send_json(
            HTTPStatus.OK,
            {
                "batches": batches,
                "default_batch": DEFAULT_BATCH,
            },
        )

    def handle_item(self, parsed) -> None:
        query = parse_qs(parsed.query)
        batch_name = query.get("batch", [DEFAULT_BATCH])[0]
        index = int(query.get("index", ["0"])[0])
        try:
            payload = current_row_payload(batch_name, index)
        except (FileNotFoundError, IndexError, ValueError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        self.send_json(HTTPStatus.OK, payload)

    def handle_first_pending(self, parsed) -> None:
        query = parse_qs(parsed.query)
        batch_name = query.get("batch", [DEFAULT_BATCH])[0]
        try:
            batch_path = batch_path_from_name(batch_name)
            rows, _ = load_rows(batch_path)
        except FileNotFoundError as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        self.send_json(
            HTTPStatus.OK,
            {
                "batch": batch_name,
                "index": first_pending_index(rows),
                "progress": summarize_rows(rows),
            },
        )

    def handle_image(self, parsed) -> None:
        query = parse_qs(parsed.query)
        batch_name = query.get("batch", [DEFAULT_BATCH])[0]
        index = int(query.get("index", ["0"])[0])
        try:
            payload = current_row_payload(batch_name, index)
        except (FileNotFoundError, IndexError, ValueError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        image_path = resolve_image_path(payload["row"].get("relative_path", ""))
        if image_path is None:
            self.send_error(HTTPStatus.NOT_FOUND, "Image not found")
            return
        data = image_path.read_bytes()
        mime_type = mimetypes.guess_type(str(image_path))[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def handle_save(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid JSON body."})
            return

        batch_name = str(payload.get("batch", DEFAULT_BATCH))
        index = int(payload.get("index", 0))
        try:
            batch_path = batch_path_from_name(batch_name)
            rows, fieldnames = load_rows(batch_path)
        except FileNotFoundError as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return

        if index < 0 or index >= len(rows):
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": f"Index out of range: {index}"})
            return

        row = dict(rows[index])
        updates = payload.get("updates", {})
        if not isinstance(updates, dict):
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "updates must be an object"})
            return

        for key, value in updates.items():
            if key not in EDITABLE_FIELDS:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": f"Field not editable: {key}"})
                return
            text_value = str(value or "").strip()
            if key == "final_router_label" and text_value not in ALLOWED_LABELS:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": f"Invalid label: {text_value}"})
                return
            if key == "final_include_in_router" and text_value not in ALLOWED_INCLUDE:
                self.send_json(
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Invalid include flag: {text_value}"},
                )
                return
            if key == "review_status" and text_value not in ALLOWED_STATUS:
                self.send_json(
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Invalid review status: {text_value}"},
                )
                return
            row[key] = text_value

        rows[index] = row
        atomic_write_rows(batch_path, fieldnames, rows)
        self.send_json(
            HTTPStatus.OK,
            {
                "message": "Saved",
                "batch": batch_name,
                "index": index,
                "progress": summarize_rows(rows),
            },
        )

    def send_json(self, status: HTTPStatus, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), ReviewerHandler)
    print(
        "Anterior view-router reviewer running at "
        f"http://{args.host}:{args.port} "
        f"(saving directly into {REVIEW_BATCH_DIR})"
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
