"""Exercise: a tiny workflow runner. Run:  pytest tests/test_w06_orchestration.py

A workflow is a dict {task_name: [names it depends on]}.
"""

# The real task graph for this repo.
PIPELINE = {
    "ingest": [],
    "transform": ["ingest"],
    "quality": ["transform"],
    "aggregate": ["quality"],
}


def topological_order(deps):
    """Return task names so every task appears after all of its dependencies.

    Raise ValueError if the graph has a cycle or depends on an unknown task.
    """
    # TODO: repeatedly pick tasks whose dependencies are all already placed
    raise NotImplementedError


def run_with_retries(fn, retries):
    """Call fn(). If it raises, call it again, up to `retries` extra times.

    Return True if any attempt succeeds, False if all attempts fail.
    """
    # TODO: loop retries + 1 times, catching Exception
    raise NotImplementedError


def run_workflow(tasks, deps, retries=0):
    """Run tasks (dict name -> callable) in dependency order.

    Return {name: "success" | "failed" | "skipped"}.
    A task is "skipped" (never called) if any dependency did not succeed.
    """
    # TODO: use topological_order, run_with_retries and a status dict
    raise NotImplementedError
