"""Exercise: ingest from a REST API into bronze. Run:  pytest tests/test_w06_api_ingest.py

The "API" is a local mock (tests/mock_weather_api.py), so no network or account is needed.
Read that file's docstring first: it tells you what the API returns and how it fails.

Uses only the standard library (urllib), so nothing new to install. The ideas are
identical with the `requests` library you will see in real projects.
"""

import json  # noqa: F401  (used once you fill in the TODOs)
import time
import urllib.error
import urllib.parse
import urllib.request  # noqa: F401


class ApiError(Exception):
    """The API call failed for good (not worth retrying, or retries ran out)."""


def fetch_json(url, retries=3, backoff=0.5, sleep=time.sleep):
    """GET `url` and return the parsed JSON body.

    - Retry (up to `retries` extra attempts) on: HTTP 429, HTTP 5xx, and network errors
      (urllib.error.URLError that is not an HTTPError).
    - Wait between attempts with exponential backoff: backoff * 2**attempt, where attempt
      starts at 0. If a 429 response has a Retry-After header, wait that many seconds instead.
    - Wait by calling `sleep(seconds)` (tests pass a fake so nothing really sleeps).
    - Any other 4xx (400, 404, ...) is the caller's bug: raise ApiError immediately, no retry.
    - When retries run out, raise ApiError.
    """
    # TODO: loop over attempts; urllib.request.urlopen(url) raises urllib.error.HTTPError
    #       for 4xx/5xx, and HTTPError has .code and .headers
    raise NotImplementedError


def fetch_all_pages(base_url, since=None, **fetch_kwargs):
    """Return every record from GET {base_url}/weather, following pagination.

    - Start at page=1. Add `since=<value>` to the query string only when since is not None.
    - Each response is {"data": [...], "next_page": <int or None>}. Keep going until
      next_page is None.
    - Build the query string with urllib.parse.urlencode (it escapes the ':' in timestamps).
    - Pass **fetch_kwargs (retries, backoff, sleep) through to fetch_json.
    """
    # TODO
    raise NotImplementedError


def to_bronze_rows(records, ingested_at, source="weather_api"):
    """Wrap raw API records as bronze rows, WITHOUT changing the payload.

    Return a list of dicts: {"source": source, "ingested_at": ingested_at, "raw": <json string>}
    where raw is json.dumps(record, sort_keys=True).

    Why keep the raw JSON as one string? Bronze is the untouched copy. If the API adds or
    renames a field tomorrow, bronze still loads; silver is where you parse and enforce a schema.
    """
    # TODO
    raise NotImplementedError


def read_watermark(path):
    """Return the saved watermark string from the JSON file at `path`, or None if no file yet.

    File format: {"watermark": "2025-02-01T00:00:10Z"}
    """
    # TODO: pathlib.Path(path).exists(), json.loads(...)
    raise NotImplementedError


def write_watermark(path, value):
    """Save {"watermark": value} to `path` as JSON."""
    # TODO
    raise NotImplementedError


def incremental_run(base_url, state_path, bronze_path, now, **fetch_kwargs):
    """One scheduled run: fetch only what is new, append it to bronze, move the watermark.

    1. since = read_watermark(state_path)  (None on the very first run -> fetch everything)
    2. records = fetch_all_pages(base_url, since=since, **fetch_kwargs)
    3. If there are no records: return 0 and leave the watermark and bronze file alone.
    4. Append one JSON line per bronze row (see to_bronze_rows, ingested_at=now) to the
       file at `bronze_path` (JSON Lines: one json.dumps(row) per line, mode "a").
    5. Set the watermark to the largest updated_at among the fetched records.
       Do this LAST: if the append crashes, the next run re-fetches the same records
       instead of silently losing them.
    6. Return how many records you appended.
    """
    # TODO
    raise NotImplementedError
