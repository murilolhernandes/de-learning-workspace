"""A tiny local stand-in for a REST weather API. Not an exercise: do not edit.

    GET /weather?page=1&since=2025-01-02T00:00:00Z

returns   {"data": [ {...record...}, ... ], "next_page": 2}     (next_page is null on the last page)

Behaviour you have to handle in the exercise:
  * results are paginated (`page_size` records per page, pages start at 1)
  * `since` is exclusive: only records with updated_at > since come back
  * it can fail on purpose: pass `failures=[429, 500]` and the first two requests
    get those status codes (a 429 also carries a `Retry-After` header)

Poke at it by hand (inside the container or anywhere with Python):
    python tests/mock_weather_api.py      # serves on http://127.0.0.1:8765
    curl "http://127.0.0.1:8765/weather?page=1"
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def make_records(n, start_day=1):
    """n deterministic weather records, one per (region, day), updated_at rising with id."""
    regions = ["south", "midwest", "east"]
    out = []
    for i in range(n):
        day = start_day + i
        out.append(
            {
                "id": day,
                "region": regions[i % 3],
                "date": f"2025-01-{(day % 28) + 1:02d}",
                "temp_f": 40 + (day * 7) % 45,
                "precip_in": round(((day * 13) % 10) / 10, 1),
                "updated_at": f"2025-02-01T00:{day // 60:02d}:{day % 60:02d}Z",
            }
        )
    return out


class MockWeatherApi:
    def __init__(self, records, page_size=10, failures=None):
        self.records = list(records)
        self.page_size = page_size
        self.failures = list(failures or [])  # status codes to return before behaving
        self.request_log = []  # every requested path+query, in order
        self._server = None

    def _handler(self):
        api = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):  # keep test output quiet
                pass

            def _send(self, status, body, headers=None):
                payload = json.dumps(body).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                for k, v in (headers or {}).items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(payload)

            def do_GET(self):
                api.request_log.append(self.path)
                if api.failures:
                    status = api.failures.pop(0)
                    headers = {"Retry-After": "2"} if status == 429 else {}
                    return self._send(status, {"error": f"injected {status}"}, headers)

                url = urlparse(self.path)
                if url.path != "/weather":
                    return self._send(404, {"error": "not found"})
                q = parse_qs(url.query)
                page = int(q.get("page", ["1"])[0])
                since = q.get("since", [None])[0]

                rows = [r for r in api.records if since is None or r["updated_at"] > since]
                start = (page - 1) * api.page_size
                chunk = rows[start : start + api.page_size]
                has_more = start + api.page_size < len(rows)
                self._send(200, {"data": chunk, "next_page": page + 1 if has_more else None})

        return Handler

    def start(self, port=0):
        self._server = HTTPServer(("127.0.0.1", port), self._handler())
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
        return self

    @property
    def url(self):
        return f"http://127.0.0.1:{self._server.server_port}"

    def stop(self):
        self._server.shutdown()
        self._server.server_close()

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc):
        self.stop()


if __name__ == "__main__":
    api = MockWeatherApi(make_records(25), page_size=10).start(port=8765)
    print(f"Mock weather API on {api.url}  (Ctrl+C to stop)")
    threading.Event().wait()
