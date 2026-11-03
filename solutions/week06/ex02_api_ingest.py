"""Solution: ingest from a REST API into bronze (stdlib only)."""

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


class ApiError(Exception):
    """The API call failed for good (not worth retrying, or retries ran out)."""


def fetch_json(url, retries=3, backoff=0.5, sleep=time.sleep):
    last = None
    for attempt in range(retries + 1):
        wait = backoff * 2**attempt
        try:
            with urllib.request.urlopen(url) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 or 500 <= e.code < 600:
                last = e
                retry_after = e.headers.get("Retry-After") if e.code == 429 else None
                if retry_after is not None:
                    wait = float(retry_after)
                    wait = int(wait) if wait.is_integer() else wait
            else:
                raise ApiError(f"HTTP {e.code} for {url}") from e
        except urllib.error.URLError as e:
            last = e
        if attempt < retries:
            sleep(wait)
    raise ApiError(f"gave up after {retries + 1} attempts: {last}") from last


def fetch_all_pages(base_url, since=None, **fetch_kwargs):
    records, page = [], 1
    while page is not None:
        params = {"page": page}
        if since is not None:
            params["since"] = since
        body = fetch_json(f"{base_url}/weather?{urllib.parse.urlencode(params)}", **fetch_kwargs)
        records.extend(body["data"])
        page = body["next_page"]
    return records


def to_bronze_rows(records, ingested_at, source="weather_api"):
    return [
        {"source": source, "ingested_at": ingested_at, "raw": json.dumps(r, sort_keys=True)}
        for r in records
    ]


def read_watermark(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text())["watermark"]


def write_watermark(path, value):
    Path(path).write_text(json.dumps({"watermark": value}))


def incremental_run(base_url, state_path, bronze_path, now, **fetch_kwargs):
    since = read_watermark(state_path)
    records = fetch_all_pages(base_url, since=since, **fetch_kwargs)
    if not records:
        return 0
    with open(bronze_path, "a") as f:
        for row in to_bronze_rows(records, now):
            f.write(json.dumps(row) + "\n")
    write_watermark(state_path, max(r["updated_at"] for r in records))
    return len(records)
