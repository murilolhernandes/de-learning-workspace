import json

import pytest
from conftest import load_exercise
from mock_weather_api import MockWeatherApi, make_records

api_mod = load_exercise("06_orchestration", "ex02_api_ingest")


class Sleeps(list):
    """Fake sleep: records the requested waits instead of waiting."""

    def __call__(self, seconds):
        self.append(seconds)


# ---------- fetch_json: retries and backoff ----------


def test_fetch_json_returns_parsed_body():
    with MockWeatherApi(make_records(3)) as api:
        body = api_mod.fetch_json(f"{api.url}/weather?page=1")
    assert [r["id"] for r in body["data"]] == [1, 2, 3]


def test_fetch_json_retries_500_with_exponential_backoff():
    sleeps = Sleeps()
    with MockWeatherApi(make_records(3), failures=[500, 503]) as api:
        body = api_mod.fetch_json(f"{api.url}/weather?page=1", retries=3, backoff=0.5, sleep=sleeps)
        assert len(api.request_log) == 3  # two failures, then success
    assert len(body["data"]) == 3
    assert sleeps == [0.5, 1.0]


def test_fetch_json_honors_retry_after_on_429():
    sleeps = Sleeps()
    with MockWeatherApi(make_records(3), failures=[429]) as api:
        api_mod.fetch_json(f"{api.url}/weather?page=1", retries=2, backoff=0.5, sleep=sleeps)
    assert sleeps == [2]  # the server said Retry-After: 2


def test_fetch_json_gives_up_after_retries():
    sleeps = Sleeps()
    with MockWeatherApi(make_records(3), failures=[500] * 10) as api:
        with pytest.raises(api_mod.ApiError):
            api_mod.fetch_json(f"{api.url}/weather?page=1", retries=2, backoff=0.1, sleep=sleeps)
        assert len(api.request_log) == 3  # 1 try + 2 retries
    assert len(sleeps) == 2


def test_fetch_json_does_not_retry_client_errors():
    sleeps = Sleeps()
    with MockWeatherApi(make_records(3)) as api:
        with pytest.raises(api_mod.ApiError):
            api_mod.fetch_json(f"{api.url}/nope", retries=3, sleep=sleeps)
        assert len(api.request_log) == 1  # a 404 is our bug; retrying cannot fix it
    assert sleeps == []


def test_fetch_json_retries_connection_errors():
    sleeps = Sleeps()
    with pytest.raises(api_mod.ApiError):
        # port 1 refuses connections
        api_mod.fetch_json("http://127.0.0.1:1/weather", retries=2, backoff=0.1, sleep=sleeps)
    assert len(sleeps) == 2


# ---------- fetch_all_pages: pagination ----------


def test_fetch_all_pages_follows_pagination():
    with MockWeatherApi(make_records(25), page_size=10) as api:
        records = api_mod.fetch_all_pages(api.url)
        assert len(api.request_log) == 3  # 10 + 10 + 5
    assert [r["id"] for r in records] == list(range(1, 26))


def test_fetch_all_pages_exact_multiple_of_page_size():
    with MockWeatherApi(make_records(20), page_size=10) as api:
        records = api_mod.fetch_all_pages(api.url)
        assert len(api.request_log) == 2
    assert len(records) == 20


def test_fetch_all_pages_empty_result():
    with MockWeatherApi([]) as api:
        assert api_mod.fetch_all_pages(api.url) == []


def test_fetch_all_pages_passes_since_and_escapes_it():
    recs = make_records(25)
    since = recs[19]["updated_at"]
    with MockWeatherApi(recs, page_size=10) as api:
        records = api_mod.fetch_all_pages(api.url, since=since)
        assert "since=2025-02-01T00%3A00%3A20Z" in api.request_log[0]
    assert [r["id"] for r in records] == [21, 22, 23, 24, 25]


def test_fetch_all_pages_retries_through_flaky_pages():
    with MockWeatherApi(make_records(15), page_size=10, failures=[500]) as api:
        records = api_mod.fetch_all_pages(api.url, retries=2, backoff=0, sleep=Sleeps())
    assert len(records) == 15


# ---------- bronze rows ----------


def test_to_bronze_rows_keeps_payload_untouched():
    recs = make_records(2)
    rows = api_mod.to_bronze_rows(recs, "2025-03-01T00:00:00Z")
    assert len(rows) == 2
    assert set(rows[0]) == {"source", "ingested_at", "raw"}
    assert rows[0]["source"] == "weather_api"
    assert rows[0]["ingested_at"] == "2025-03-01T00:00:00Z"
    assert json.loads(rows[0]["raw"]) == recs[0]


def test_to_bronze_rows_survives_new_fields():
    rec = {**make_records(1)[0], "wind_mph": 12}  # the API added a column
    rows = api_mod.to_bronze_rows([rec], "t")
    assert json.loads(rows[0]["raw"])["wind_mph"] == 12


# ---------- watermark ----------


def test_watermark_missing_then_roundtrip(tmp_path):
    p = tmp_path / "state.json"
    assert api_mod.read_watermark(p) is None
    api_mod.write_watermark(p, "2025-02-01T00:00:10Z")
    assert api_mod.read_watermark(p) == "2025-02-01T00:00:10Z"
    assert json.loads(p.read_text()) == {"watermark": "2025-02-01T00:00:10Z"}


# ---------- incremental_run ----------


def _lines(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def test_incremental_run_first_run_loads_everything(tmp_path):
    state, bronze = tmp_path / "state.json", tmp_path / "bronze.jsonl"
    recs = make_records(25)
    with MockWeatherApi(recs, page_size=10) as api:
        n = api_mod.incremental_run(api.url, state, bronze, now="2025-03-01T00:00:00Z")
    assert n == 25
    assert len(_lines(bronze)) == 25
    assert api_mod.read_watermark(state) == recs[-1]["updated_at"]


def test_incremental_run_is_idempotent_when_nothing_new(tmp_path):
    state, bronze = tmp_path / "state.json", tmp_path / "bronze.jsonl"
    with MockWeatherApi(make_records(12), page_size=10) as api:
        api_mod.incremental_run(api.url, state, bronze, now="t1")
        before = bronze.read_text()
        n = api_mod.incremental_run(api.url, state, bronze, now="t2")
    assert n == 0
    assert bronze.read_text() == before  # no duplicates on a re-run


def test_incremental_run_picks_up_only_new_records(tmp_path):
    state, bronze = tmp_path / "state.json", tmp_path / "bronze.jsonl"
    with MockWeatherApi(make_records(10), page_size=4) as api:
        api_mod.incremental_run(api.url, state, bronze, now="t1")
        api.records += make_records(3, start_day=11)  # three new records arrive upstream
        n = api_mod.incremental_run(api.url, state, bronze, now="t2")
    assert n == 3
    rows = _lines(bronze)
    assert len(rows) == 13
    assert [r["ingested_at"] for r in rows] == ["t1"] * 10 + ["t2"] * 3
    assert [json.loads(r["raw"])["id"] for r in rows] == list(range(1, 14))


def test_incremental_run_failure_does_not_move_watermark(tmp_path):
    state, bronze = tmp_path / "state.json", tmp_path / "bronze.jsonl"
    with MockWeatherApi(make_records(5), failures=[500] * 10) as api:
        with pytest.raises(api_mod.ApiError):
            api_mod.incremental_run(api.url, state, bronze, now="t1", retries=1, backoff=0, sleep=Sleeps())
    assert api_mod.read_watermark(state) is None
    assert not bronze.exists()
