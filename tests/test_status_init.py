"""foundry-init and foundry-status (bin/)."""
import json
import os
import subprocess
import sys

from conftest import PLUGIN, init, run

STATUS = [sys.executable, os.path.join(PLUGIN, "bin", "foundry-status")]


def test_session_start_silent_without_foundry(project):
    r = run(STATUS + ["--session-start"], project)
    assert r.returncode == 0 and r.stdout == ""


def test_init_layout(project):
    r = init(project, "toy", "src/toy", level="L2")
    assert r.returncode == 0, r.stderr
    cd = project / "foundry" / "toy"
    cfg = json.loads((cd / "foundry.json").read_text())
    assert cfg["source"] == ["src/toy"] and cfg["level"] == "L2"
    for d in ["spec/issues", "tests/public", "tests/holdout", "reference", "audit/private", "scripts", "progress"]:
        assert (cd / d).is_dir(), d
    assert (cd / "pages").is_dir()
    for f in ["model.md", "terms.md", "acceptance.md", "project.md", "overview.md"]:
        assert (cd / "spec" / f).is_file(), f
    for f in ["build", "run-public-tests", "run-holdout", "run-oracle", "mutate"]:
        assert os.access(cd / "scripts" / f, os.X_OK), f


def test_init_refuses(project):
    assert init(project, "toy", "src/toy").returncode == 0
    assert init(project, "toy", "src/toy").returncode != 0          # exists
    assert init(project, "Bad Name", "src").returncode != 0         # name
    assert init(project, "x", "../outside").returncode != 0         # source outside project


def test_status_and_rules(project):
    init(project, "toy", "src/toy")
    r = run(STATUS + ["--session-start"], project)
    assert "toy" in r.stdout and "stage: 1 spec" in r.stdout and "orchestrator rules" in r.stdout


def write_review(path, approved):
    path.write_text("# Review\n\n- Review status: " + ("APPROVED (x)" if approved else "IN REVIEW") +
                    "\n\n## [1/1] a\n- Status: APPROVED\n- Verified: n/a\n")


def test_stage_progression_and_git_staleness(project):
    init(project, "toy", "src/toy")
    cd = project / "foundry" / "toy"
    (project / "src" / "toy").mkdir(parents=True)
    (project / "src/toy/m.py").write_text("x = 1\n")
    write_review(cd / "spec/REVIEW.md", True)
    write_review(cd / "tests/REVIEW.md", True)
    git = lambda *a: subprocess.run(["git", *a], cwd=project, check=True, capture_output=True)  # noqa: E731
    git("add", "-A"); git("commit", "-qm", "c1")
    assert "stage: 3 develop" in run(STATUS, project).stdout
    (cd / "audit/verdict.md").write_text("PASS\n")
    git("add", "-A"); git("commit", "-qm", "audit")
    assert "stage: 4 report" in run(STATUS, project).stdout
    write_review(cd / "audit/REVIEW.md", True)
    git("add", "-A"); git("commit", "-qm", "report")
    assert "stage: done" in run(STATUS, project).stdout
    (project / "src/toy/m.py").write_text("x = 2\n")              # uncommitted change after audit
    assert "changed after the last audit" in run(STATUS, project).stdout
    git("add", "-A"); git("commit", "-qm", "later")               # committed change after audit
    assert "changed after the last audit" in run(STATUS, project).stdout


def test_open_spec_issue_wins(project):
    init(project, "toy", "src/toy")
    (project / "foundry/toy/spec/issues/001-x.md").write_text("# 001\n")
    assert "stage: spec issues" in run(STATUS, project).stdout


def test_with_rules_always_prints(project):
    """foundry:start injects `foundry-status --with-rules`; it must print the rules even with no code yet
    (skills may not `cat` files outside the working directory, so the rules come through this command)."""
    r = run(STATUS + ["--with-rules"], project)
    assert r.returncode == 0 and "orchestrator rules" in r.stdout and "no code in this project yet" in r.stdout
