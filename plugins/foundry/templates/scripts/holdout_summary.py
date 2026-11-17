"""pytest plugin for scripts/run-holdout: counts results per meta.kind.

Writes only `kind=<k> pass=<p> fail=<f>` lines (k = 1..6, none) and a
`total` line to the file named by $HOLDOUT_SUMMARY. No test names, inputs,
values or messages are written there.
"""
import os
from collections import defaultdict

_kind_of = {}
_result = {}            # nodeid -> "pass" | "fail"
_collect_errors = 0


def _kind(item):
    m = item.get_closest_marker("meta")
    k = m.kwargs.get("kind") if m else None
    return str(k) if k in (1, 2, 3, 4, 5, 6) else "none"


def pytest_collection_modifyitems(items):
    for it in items:
        _kind_of[it.nodeid] = _kind(it)


def pytest_collectreport(report):
    global _collect_errors
    if report.failed:
        _collect_errors += 1


def pytest_runtest_logreport(report):
    prev = _result.get(report.nodeid)
    if report.failed or report.skipped:
        _result[report.nodeid] = "fail"
    elif report.when == "call" and prev != "fail":
        _result[report.nodeid] = "pass"


def pytest_sessionfinish(session):
    counts = defaultdict(lambda: [0, 0])
    for nodeid, kind in _kind_of.items():
        r = _result.get(nodeid, "fail")
        counts[kind][0 if r == "pass" else 1] += 1
    counts["none"][1] += _collect_errors
    lines, tp, tf = [], 0, 0
    for k in ["1", "2", "3", "4", "5", "6", "none"]:
        p, f = counts[k] if k in counts else (0, 0)
        if k != "none" or p or f:
            lines.append(f"kind={k} pass={p} fail={f}")
        tp, tf = tp + p, tf + f
    lines.append(f"total pass={tp} fail={tf}")
    path = os.environ.get("HOLDOUT_SUMMARY")
    if path:
        with open(path, "w") as fh:
            fh.write("\n".join(lines) + "\n")
