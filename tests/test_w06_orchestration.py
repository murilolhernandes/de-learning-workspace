import pytest
from conftest import load_exercise

wf = load_exercise("06_orchestration", "ex01_workflow")


def test_topological_order_respects_dependencies():
    order = wf.topological_order(wf.PIPELINE)
    assert order == ["ingest", "transform", "quality", "aggregate"]


def test_topological_order_diamond():
    deps = {"a": [], "b": ["a"], "c": ["a"], "d": ["b", "c"]}
    order = wf.topological_order(deps)
    assert order.index("a") < order.index("b") < order.index("d")
    assert order.index("a") < order.index("c") < order.index("d")


def test_cycle_raises():
    with pytest.raises(ValueError):
        wf.topological_order({"a": ["b"], "b": ["a"]})


def test_unknown_dependency_raises():
    with pytest.raises(ValueError):
        wf.topological_order({"a": ["ghost"]})


def test_retry_succeeds_after_failures():
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("transient")

    assert wf.run_with_retries(flaky, retries=2) is True
    assert len(calls) == 3


def test_retry_gives_up():
    def broken():
        raise RuntimeError("always")

    assert wf.run_with_retries(broken, retries=1) is False


def test_workflow_runs_in_order():
    log = []
    tasks = {n: (lambda n=n: log.append(n)) for n in wf.PIPELINE}
    result = wf.run_workflow(tasks, wf.PIPELINE)
    assert log == ["ingest", "transform", "quality", "aggregate"]
    assert set(result.values()) == {"success"}


def test_failure_skips_downstream():
    log = []

    def bad():
        raise RuntimeError("boom")

    tasks = {
        "ingest": lambda: log.append("ingest"),
        "transform": bad,
        "quality": lambda: log.append("quality"),
        "aggregate": lambda: log.append("aggregate"),
    }
    result = wf.run_workflow(tasks, wf.PIPELINE)
    assert result == {
        "ingest": "success",
        "transform": "failed",
        "quality": "skipped",
        "aggregate": "skipped",
    }
    assert log == ["ingest"]
