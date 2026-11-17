"""Information barriers (hooks/guard.py)."""
import pytest

from conftest import call, hook

P = "{p}"  # placeholder for the project path in absolute file paths


def a(project, rel):
    return str(project / rel)


CASES = [
    # (agent, tool, field, value, allowed)
    ("foundry:developer", "Read", "file_path", "foundry/alpha/tests/holdout/a.json", False),
    ("foundry:developer", "Read", "file_path", "foundry/beta/tests/generators/g.py", False),
    ("foundry:developer", "Read", "file_path", "foundry/beta/reference/o.py", False),
    ("foundry:developer", "Read", "file_path", "foundry/alpha/audit/private/x.log", False),
    ("foundry:developer", "Read", "file_path", "foundry/alpha/tests/public/a.json", True),
    ("foundry:developer", "Read", "file_path", "foundry/alpha/audit/holdout.md", True),
    ("foundry:developer", "Write", "file_path", "alpha/src/m.py", True),
    ("foundry:developer", "Write", "file_path", "lib/beta/m.py", True),
    ("foundry:developer", "Write", "file_path", "foundry/alpha/tests/public/a.py", False),
    ("foundry:developer", "Write", "file_path", "foundry/alpha/tests/regression/new.py", True),
    ("foundry:developer", "Edit", "file_path", "foundry/alpha/tests/regression/old.py", False),
    ("foundry:developer", "Write", "file_path", "foundry/alpha/foundry.json", False),
    ("foundry:developer", "Write", "file_path", "foundry/alpha/scripts/build", False),
    ("foundry:developer", "Write", "file_path", "foundry/alpha/spec/issues/001-x.md", True),
    ("foundry:developer", "Write", "file_path", "foundry/alpha/progress/developer.md", True),
    ("developer", "Read", "file_path", "foundry/alpha/tests/holdout/a.json", False),  # bare name too
    ("foundry:oracle", "Read", "file_path", "lib/beta/m.py", False),
    ("foundry:oracle", "Read", "file_path", "foundry/beta/tests/public/a", False),
    ("foundry:oracle", "Write", "file_path", "foundry/beta/reference/o.py", True),
    ("foundry:oracle", "Write", "file_path", "lib/beta/m.py", False),
    ("foundry:test-designer", "Read", "file_path", "alpha/src/m.py", False),
    ("foundry:test-designer", "Read", "file_path", "foundry/alpha/reference/o.py", False),
    ("foundry:test-designer", "Write", "file_path", "foundry/alpha/tests/generators/g.py", True),
    ("foundry:test-designer", "Write", "file_path", "/tmp/outside.py", False),
    ("foundry:spec-writer", "Write", "file_path", "foundry/alpha/spec/model.md", True),
    ("foundry:spec-writer", "Write", "file_path", "foundry/alpha/tests/x.py", False),
    ("foundry:auditor", "Read", "file_path", "foundry/alpha/tests/holdout/a.json", True),
    ("foundry:auditor", "Write", "file_path", "foundry/alpha/audit/verdict.md", True),
    ("foundry:auditor", "Edit", "file_path", "alpha/src/m.py", False),
    ("foundry:auditor", "Edit", "file_path", "foundry/alpha/spec/model.md", False),
    (None, "Read", "file_path", "foundry/alpha/tests/holdout/a.json", True),  # main session
    ("Explore", "Read", "file_path", "foundry/alpha/tests/holdout/a.json", True),  # non-workflow agent
]


@pytest.mark.parametrize("agent,tool,field,value,allowed", CASES)
def test_file_access(two_codes, agent, tool, field, value, allowed):
    path = value if value.startswith("/") else str(two_codes / value)
    ok, err = hook("guard.py", two_codes, call(agent, tool, **{field: path}))
    assert ok == allowed, err


def test_search_scope(two_codes):
    ok, _ = hook("guard.py", two_codes, call("foundry:developer", "Grep", pattern="x"))
    assert not ok  # project root contains forbidden paths
    ok, _ = hook("guard.py", two_codes, call("foundry:developer", "Grep", pattern="x", path=str(two_codes / "alpha/src")))
    assert ok
    ok, _ = hook("guard.py", two_codes, call("foundry:developer", "Glob", pattern="foundry/alpha/tests/holdout/**",
                                            path=str(two_codes / "foundry/alpha/tests/public")))
    assert not ok


BASH = [
    ("foundry/alpha/scripts/run-public-tests -x -q", True),
    ("./foundry/alpha/scripts/build", True),
    ("foundry/alpha/scripts/run-public-tests; cat foundry/alpha/tests/holdout/a", False),
    ("foundry/alpha/scripts/../../x/scripts/build", False),
    ("foundry/alpha/scripts/run-holdout", False),
    ("git status", True),
    ("git log --oneline -n 5", True),
    ("git log -p", False),
    ("git diff -- alpha/src", True),
    ("git diff --stat -- lib/beta/m.py", True),
    ("git diff -- foundry/alpha/tests/holdout", False),
    ("git diff -- alpha/src/../../foundry/alpha/tests/holdout", False),
    ("git show HEAD:foundry/alpha/tests/holdout/a", False),
    ("ls -R", False),
]


@pytest.mark.parametrize("cmd,allowed", BASH)
def test_developer_bash(two_codes, cmd, allowed):
    ok, err = hook("guard.py", two_codes, call("foundry:developer", "Bash", command=cmd))
    assert ok == allowed, err


@pytest.mark.parametrize("agent,cmd,allowed", [
    ("foundry:oracle", "cat lib/beta/m.py", False),
    ("foundry:oracle", "python3 foundry/beta/reference/selfcheck.py", True),
    ("foundry:test-designer", "foundry/alpha/scripts/run-oracle in.json", True),
    ("foundry:test-designer", "grep -r x alpha/src", False),
])
def test_other_bash(two_codes, agent, cmd, allowed):
    ok, err = hook("guard.py", two_codes, call(agent, "Bash", command=cmd))
    assert ok == allowed, err


def test_inactive_without_foundry(project):
    ok, _ = hook("guard.py", project, call("foundry:developer", "Bash", command="ls -R"))
    assert ok


@pytest.mark.parametrize("agent", ["foundry:spec-writer", "foundry:test-designer", "foundry:auditor", "foundry:developer"])
def test_pages_are_orchestrator_only(two_codes, agent):
    ok, _ = hook("guard.py", two_codes, call(agent, "Write", file_path=str(two_codes / "foundry/alpha/pages/spec.html")))
    assert not ok
