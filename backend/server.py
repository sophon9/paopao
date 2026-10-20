"""Serve the practice app and the quiz API on one port."""

import json
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.papers import create_paper, get_paper, home_summary, submit_paper

STATIC_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _json(self, code, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            self._json(200, {"ok": True})
            return
        if path == "/api/home":
            try:
                self._json(200, home_summary())
            except Exception as exc:
                self._json(500, {"error": str(exc)})
            return
        if path.startswith("/api/papers/") and path.count("/") == 3:
            try:
                paper_id = int(path.rstrip("/").split("/")[3])
                self._json(200, get_paper(paper_id))
            except ValueError as exc:
                self._json(404, {"error": str(exc)})
            except Exception as exc:
                self._json(500, {"error": str(exc)})
            return
        self._static(path)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self._read_json()
        except json.JSONDecodeError:
            self._json(400, {"error": "ข้อมูลที่ส่งมาอ่านไม่ได้"})
            return
        try:
            if path == "/api/papers":
                payload = create_paper(
                    mode=body.get("mode"),
                    subject=body.get("subject"),
                    topic=body.get("topic"),
                    timer=bool(body.get("timer", True)),
                )
                self._json(200, payload)
                return
            if path.startswith("/api/papers/") and path.endswith("/submit"):
                paper_id = int(path.split("/")[3])
                payload = submit_paper(
                    paper_id,
                    body.get("answers"),
                    body.get("usedSec") or 0,
                    bool(body.get("auto")),
                )
                self._json(200, payload)
                return
        except ValueError as exc:
            self._json(400, {"error": str(exc)})
            return
        except Exception as exc:
            self._json(500, {"error": str(exc)})
            return
        self._json(404, {"error": "ไม่พบรายการ"})

    def _static(self, path):
        rel = path.lstrip("/") or "index.html"
        target = (ROOT / rel).resolve()
        if target != ROOT and ROOT not in target.parents:
            self._json(403, {"error": "ห้ามเข้า"})
            return
        if "backend" in target.parts or target.suffix == ".db":
            self._json(404, {"error": "ไม่พบไฟล์"})
            return
        if target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            self._json(404, {"error": "ไม่พบไฟล์"})
            return
        data = target.read_bytes()
        mime = STATIC_TYPES.get(target.suffix, mimetypes.guess_type(target.name)[0] or "application/octet-stream")
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Suankularb practice server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8082)
    args = parser.parse_args()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Practice app at http://127.0.0.1:{args.port}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("stopped", flush=True)


if __name__ == "__main__":
    main()
