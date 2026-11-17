"""Shared fixtures: a throw-away project with foundry code folders, and hook runners."""
import json
import os
import subprocess
import sys

import pytest

PLUGIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugins", "foundry")


def run(cmd, project, stdin=None, env_extra=None):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project), **(env_extra or {}))
    return subprocess.run(cmd, input=stdin, capture_output=True, text=True, cwd=project, env=env)


def init(project, code, *sources, level=None):
    cmd = [sys.executable, os.path.join(PLUGIN, "bin", "foundry-init"), code]
    for s in sources:
        cmd += ["--source", s]
    if level:
        cmd += ["--level", level]
    return run(cmd, project)


@pytest.fixture
def project(tmp_path):
    """An empty git project."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    return tmp_path


@pytest.fixture
def two_codes(project):
    """Project with codes 'alpha' (main code alpha/src) and 'beta' (main code lib/beta)."""
    assert init(project, "alpha", "alpha/src").returncode == 0
    assert init(project, "beta", "lib/beta", level="L2").returncode == 0
    (project / "alpha" / "src").mkdir(parents=True)
    (project / "lib" / "beta").mkdir(parents=True)
    (project / "foundry/alpha/tests/regression/old.py").write_text("x = 1\n")
    return project


def hook(script, project, payload):
    """Run a PreToolUse hook; return (allowed, stderr)."""
    r = run([sys.executable, os.path.join(PLUGIN, "hooks", script)], project, stdin=json.dumps(payload))
    return r.returncode == 0, r.stderr


def call(agent, tool, **tool_input):
    d = {"tool_name": tool, "tool_input": tool_input}
    if agent:
        d["agent_type"] = agent
    return d
