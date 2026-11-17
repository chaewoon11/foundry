"""Plugin and marketplace manifests."""
import json
import os
import shutil
import subprocess

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_manifests_consistent():
    m = json.load(open(os.path.join(ROOT, ".claude-plugin/marketplace.json")))
    p = json.load(open(os.path.join(ROOT, "plugins/foundry/.claude-plugin/plugin.json")))
    entry = next(e for e in m["plugins"] if e["name"] == "foundry")
    assert entry["source"] == "./plugins/foundry" and p["name"] == "foundry"
    hooks = json.load(open(os.path.join(ROOT, "plugins/foundry/hooks/hooks.json")))
    assert set(hooks["hooks"]) == {"SessionStart", "PreToolUse"}


@pytest.mark.skipif(shutil.which("claude") is None, reason="claude CLI not installed")
@pytest.mark.parametrize("target", [".", "plugins/foundry"])
def test_claude_validate(target):
    r = subprocess.run(["claude", "plugin", "validate", target], cwd=ROOT, capture_output=True, text=True)
    assert "Validation passed" in r.stdout + r.stderr, r.stdout + r.stderr
