"""Tests for the foundry information barrier and session-start hook."""
import json
import os
import subprocess
import sys

import pytest

HOOKS = os.path.join(os.path.dirname(__file__), "..", "plugins", "foundry", "hooks")
GUARD = os.path.join(HOOKS, "guard.py")
START = os.path.join(HOOKS, "session_start.py")


@pytest.fixture
def proj(tmp_path):
    c = tmp_path / "foundry" / "tb"
    for d in ["theory/checks", "reference", "features/soc/tests/holdout", "features/soc/tests/public",
              "features/soc/tests/generators", "features/soc/tests/regression", "features/soc/audit/private",
              "features/soc/progress"]:
        (c / d).mkdir(parents=True)
    (c / "foundry.json").write_text(json.dumps({"code": "tb", "source": ["src/tb"]}))
    (c / "theory/derivation.md").write_text("x")
    (c / "features/soc/tests/regression/old.py").write_text("x")
    (tmp_path / "src/tb").mkdir(parents=True)
    return tmp_path


def run(proj, agent, tool, **inp):
    data = {"agent_type": agent, "tool_name": tool, "tool_input": inp, "cwd": str(proj)}
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(proj))
    r = subprocess.run([sys.executable, GUARD], input=json.dumps(data), capture_output=True, text=True, env=env)
    return r.returncode


A, B = 0, 2  # allowed, blocked
F = "foundry/tb/features/soc/"


@pytest.mark.parametrize("agent,tool,inp,want", [
    # main session and unknown agents are free
    ("", "Read", {"file_path": F + "tests/holdout/t.py"}, A),
    ("general-purpose", "Read", {"file_path": F + "tests/holdout/t.py"}, A),
    # developer
    ("foundry:developer", "Read", {"file_path": F + "tests/holdout/t.py"}, B),
    ("foundry:developer", "Read", {"file_path": F + "tests/rules.md"}, B),
    ("foundry:developer", "Read", {"file_path": F + "tests/public/t.py"}, A),
    ("foundry:developer", "Read", {"file_path": "foundry/tb/reference/o.py"}, B),
    ("foundry:developer", "Read", {"file_path": F + "audit/private/x.md"}, B),
    ("foundry:developer", "Read", {"file_path": F + "../soc/tests/holdout/t.py"}, B),
    ("foundry:developer", "Write", {"file_path": "src/tb/h.py"}, A),
    ("foundry:developer", "Edit", {"file_path": F + "tests/public/t.py"}, B),
    ("foundry:developer", "Write", {"file_path": F + "tests/regression/new.py"}, A),
    ("foundry:developer", "Write", {"file_path": F + "tests/regression/old.py"}, B),
    ("foundry:developer", "Write", {"file_path": "foundry/tb/foundry.json"}, B),
    ("foundry:developer", "Grep", {"pattern": "x", "path": F + "tests"}, B),
    ("foundry:developer", "Grep", {"pattern": "x", "path": F + "tests/public"}, A),
    ("foundry:developer", "Glob", {"pattern": "**/holdout/*"}, B),
    ("foundry:developer", "Bash", {"command": "cat " + F + "tests/holdout/t.py"}, B),
    ("foundry:developer", "Bash", {"command": "python -m pytest " + F + "tests/public"}, A),
    ("foundry:developer", "Bash", {"command": "git log -p"}, B),
    ("foundry:developer", "Bash", {"command": "git show HEAD~2"}, B),
    ("foundry:developer", "Bash", {"command": "grep -rn energy ."}, B),
    ("foundry:developer", "Bash", {"command": "cat foundry/tb/features/*/tests/h*/t.py"}, B),
    ("foundry:developer", "Bash", {"command": "git status"}, A),
    ("foundry:developer", "Bash", {"command": "git diff -- src/tb"}, A),
    # test designer: no code, no oracle; may run the existing code
    ("foundry:test-designer", "Read", {"file_path": "src/tb/h.py"}, B),
    ("foundry:test-designer", "Read", {"file_path": "foundry/tb/reference/o.py"}, B),
    ("foundry:test-designer", "Write", {"file_path": F + "tests/holdout/t.py"}, A),
    ("foundry:test-designer", "Write", {"file_path": F + "method.md"}, B),
    ("foundry:test-designer", "Bash", {"command": "python src/tb/run.py in.json"}, A),
    ("foundry:test-designer", "Bash", {"command": "cat src/tb/h.py"}, B),
    ("foundry:test-designer", "Grep", {"pattern": "x"}, B),
    # oracle: no code, no tests
    ("foundry:oracle", "Read", {"file_path": F + "tests/public/t.py"}, B),
    ("foundry:oracle", "Read", {"file_path": F + "method.md"}, A),
    ("foundry:oracle", "Write", {"file_path": "foundry/tb/reference/o.py"}, A),
    # spec writer
    ("foundry:spec-writer", "Write", {"file_path": F + "method.md"}, A),
    ("foundry:spec-writer", "Read", {"file_path": "src/tb/h.py"}, B),
    ("foundry:spec-writer", "Read", {"file_path": "foundry/tb/theory/claims.md"}, A),
    # theory checker: not the derivation it checks
    ("foundry:theory-checker", "Read", {"file_path": "foundry/tb/theory/derivation.md"}, B),
    ("foundry:theory-checker", "Read", {"file_path": "foundry/tb/theory/claims.md"}, A),
    ("foundry:theory-checker", "Bash", {"command": "cat foundry/tb/theory/derivation.md"}, B),
    ("foundry:theory-checker", "Write", {"file_path": "foundry/tb/theory/checks/C1_check.py"}, A),
    ("foundry:theory-checker", "Write", {"file_path": "foundry/tb/theory/claims.md"}, B),
    # auditor reads all, writes audit only
    ("foundry:auditor", "Read", {"file_path": F + "tests/holdout/t.py"}, A),
    ("foundry:auditor", "Write", {"file_path": F + "audit/verdict.md"}, A),
    ("foundry:auditor", "Write", {"file_path": "src/tb/h.py"}, B),
])
def test_guard(proj, agent, tool, inp, want):
    assert run(proj, agent, tool, **inp) == want


def test_no_foundry_folder_means_no_restriction(tmp_path):
    assert run(tmp_path, "foundry:developer", "Read", file_path="x/tests/holdout/t.py") == A


def test_session_start(proj):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(proj))
    out = subprocess.run([sys.executable, START], capture_output=True, text=True, env=env).stdout
    assert "tb" in out and "foundry:orchestrator" in out
    (proj / "foundry/tb/foundry.json").unlink()
    out = subprocess.run([sys.executable, START], capture_output=True, text=True, env=env).stdout
    assert "No foundry.json" in out


def test_manifests():
    root = os.path.join(os.path.dirname(__file__), "..")
    m = json.load(open(os.path.join(root, ".claude-plugin/marketplace.json")))
    src = m["plugins"][0]["source"]
    p = json.load(open(os.path.join(root, src, ".claude-plugin/plugin.json")))
    assert p["name"] == m["plugins"][0]["name"] == "foundry"
    skills = os.path.join(root, src, "skills")
    for s in os.listdir(skills):
        head = open(os.path.join(skills, s, "SKILL.md")).read().split("---")[1]
        assert f"name: {s}" in head and "description:" in head
