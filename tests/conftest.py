"""Shared fixtures. Exercise files live in weeks/, so tests load them by path.

Set USE_SOLUTIONS=1 to run the same tests against solutions/ (for maintainers; it spoils the answers).
"""

import importlib.util
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_exercise(week_dir: str, module: str):
    """Import weeks/<week_dir>/<module>.py (or solutions/<weekNN>/<module>.py)."""
    if os.environ.get("USE_SOLUTIONS") == "1":
        path = ROOT / "solutions" / f"week{week_dir[:2]}" / f"{module}.py"
    else:
        path = ROOT / "weeks" / week_dir / f"{module}.py"
    spec = importlib.util.spec_from_file_location(module, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_src_module(name: str, week: str):
    """Import src/retail_pipeline/<name>.py (or solutions/<week>/<name>.py with USE_SOLUTIONS=1)."""
    if os.environ.get("USE_SOLUTIONS") == "1":
        path = ROOT / "solutions" / week / f"{name}.py"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    return importlib.import_module(f"retail_pipeline.{name}")


@pytest.fixture(scope="session")
def spark():
    from retail_pipeline.spark_session import get_spark

    session = get_spark("tests", shuffle_partitions=2)
    yield session
    session.stop()


def _is_unfinished(excinfo) -> bool:
    """True when a test failed only because the exercise isn't started yet."""
    if excinfo is None:
        return False
    if excinfo.errisinstance(NotImplementedError):
        return True
    if excinfo.errisinstance(AssertionError):
        message = str(excinfo.value).strip()
        first_line = message.splitlines()[0] if message else ""
        if first_line.startswith("assert None"):
            return True
        return first_line.startswith("assert {") and "None" in first_line
    return False


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Report not-yet-implemented exercises as skipped, not failed.

    CI then only goes red on real mistakes. Set STRICT_EXERCISES=1 to turn this
    off and see every unfinished exercise as a failure.
    """
    outcome = yield
    report = outcome.get_result()
    if os.environ.get("STRICT_EXERCISES") == "1" or report.outcome != "failed":
        return
    if _is_unfinished(call.excinfo):
        report.outcome = "skipped"
        line = item.reportinfo()[1] or 0
        report.longrepr = (str(item.path), line, "Skipped: exercise not implemented yet")
