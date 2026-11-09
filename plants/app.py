"""Throwaway app for r2test2's Part B CHECK (B3/B4). Never deployed: .github/workflows/plants.yml and
tests/plants/ start it on 127.0.0.1 only. Standard library only, so the scanners see no new dependencies.
  PLANT 1 (fixed): no X-Content-Type-Options header (ZAP rule 10021).
  PLANT 2 (fixed): GET /api/orders answered without a token.
Delete plants/, tests/plants/ and .github/workflows/plants.yml after the check."""
import json
import os
import secrets
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = os.environ.get("PLANTS_TOKEN") or secrets.token_urlsafe(16)
HEADERS = {
    "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'",
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Referrer-Policy": "no-referrer",
    "Cross-Origin-Embedder-Policy": "require-corp",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Cache-Control": "no-store",
}
PAGES = {  # a few linked HTML pages, so ZAP's passive header check sees more than one response
    path: f"<!doctype html><html lang=en><head><meta charset=utf-8><title>{title}</title></head><body><h1>{title}</h1>"
          '<p><a href="/">Plants</a> <a href="/ferns">Ferns</a> <a href="/cacti">Cacti</a> <a href="/care">Care</a></p></body></html>'.encode()
    for path, title in {"/": "Plants", "/ferns": "Ferns", "/cacti": "Cacti", "/care": "Care"}.items()}
ORDERS = [{"id": 1, "plant": "fern", "qty": 2}]


class Handler(BaseHTTPRequestHandler):
    server_version, sys_version = "plants", ""

    def reply(self, code, body, ctype="application/json"):
        self.send_response(code)
        for k, v in HEADERS.items():
            self.send_header(k, v)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in PAGES:
            return self.reply(200, PAGES[self.path], "text/html; charset=utf-8")
        if self.path == "/api/orders":
            if self.headers.get("Authorization") != f"Bearer {TOKEN}":
                return self.reply(401, b'{"detail": "sign in"}')
            return self.reply(200, json.dumps(ORDERS).encode())
        return self.reply(404, b'{"detail": "not found"}')

    def log_message(self, *args):
        pass


def serve(port=8000):
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    serve(int(sys.argv[1]) if len(sys.argv) > 1 else 8000).serve_forever()
