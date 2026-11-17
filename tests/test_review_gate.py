"""Approval gate for REVIEW.md (hooks/review_gate.py)."""
import pytest

from conftest import call, hook

REVIEW = """# Review: spec

- Review status: IN REVIEW

## [1/2] model.md — a
- Tag: 🟡
- Status: {s1}
- Human:
- Decision:
- Edits needed:
- Verified: {v1}

## [2/2] terms.md — b
- Tag: 🟢
- Status: {s2}
- Human:
- Decision:
- Edits needed:
- Verified: n/a
"""


@pytest.fixture
def review(project):
    p = project / "REVIEW.md"
    p.write_text(REVIEW.format(s1="CHANGED", v1="no", s2="PENDING"))
    return p


def approve(text):
    return text.replace("- Review status: IN REVIEW", "- Review status: APPROVED (today)")


def test_cannot_approve_with_open_items(project, review):
    ok, err = hook("review_gate.py", project, call(None, "Write", file_path=str(review), content=approve(review.read_text())))
    assert not ok and "[2] PENDING" in err


def test_cannot_approve_unverified_change(project, review):
    text = REVIEW.format(s1="CHANGED", v1="no", s2="APPROVED")
    ok, err = hook("review_gate.py", project, call(None, "Write", file_path=str(review), content=approve(text)))
    assert not ok and "not verified" in err


def test_can_approve_when_all_decided(project, review):
    text = REVIEW.format(s1="CHANGED", v1="yes", s2="APPROVED")
    ok, err = hook("review_gate.py", project, call(None, "Write", file_path=str(review), content=approve(text)))
    assert ok, err


def test_agent_cannot_decide(project, review):
    ok, _ = hook("review_gate.py", project, call("foundry:spec-writer", "Edit", file_path=str(review),
                                               old_string="- Status: PENDING", new_string="- Status: APPROVED"))
    assert not ok


def test_agent_can_append_pending(project, review):
    new = review.read_text() + "\n## [3/3] x — c\n- Tag: 🟡\n- Status: PENDING\n- Verified: n/a\n"
    ok, err = hook("review_gate.py", project, call("foundry:spec-writer", "Write", file_path=str(review), content=new))
    assert ok, err


@pytest.mark.parametrize("cmd,allowed", [
    ("sed -i 's/IN REVIEW/APPROVED/' REVIEW.md", False),
    ("echo x >> spec/REVIEW.md", False),
    ("python3 -c 'open(\"REVIEW.md\",\"w\")'", False),
    ("cat REVIEW.md", True),
    ("grep Status spec/REVIEW.md", True),
])
def test_bash_cannot_modify_review(project, cmd, allowed):
    ok, _ = hook("review_gate.py", project, call(None, "Bash", command=cmd))
    assert ok == allowed
