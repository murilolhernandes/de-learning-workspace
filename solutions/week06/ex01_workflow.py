"""Solution: a tiny workflow runner."""

PIPELINE = {
    "ingest": [],
    "transform": ["ingest"],
    "quality": ["transform"],
    "aggregate": ["quality"],
}


def topological_order(deps):
    for name, parents in deps.items():
        for parent in parents:
            if parent not in deps:
                raise ValueError(f"{name} depends on unknown task {parent}")
    placed = []
    remaining = dict(deps)
    while remaining:
        ready = [n for n, parents in remaining.items() if all(p in placed for p in parents)]
        if not ready:
            raise ValueError("cycle detected")
        for name in ready:
            placed.append(name)
            del remaining[name]
    return placed


def run_with_retries(fn, retries):
    for _ in range(retries + 1):
        try:
            fn()
            return True
        except Exception:
            continue
    return False


def run_workflow(tasks, deps, retries=0):
    status = {}
    for name in topological_order(deps):
        if any(status[p] != "success" for p in deps[name]):
            status[name] = "skipped"
        elif run_with_retries(tasks[name], retries):
            status[name] = "success"
        else:
            status[name] = "failed"
    return status
