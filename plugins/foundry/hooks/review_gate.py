#!/usr/bin/env python3
"""Approval gate for review records (PreToolUse on Write/Edit).

Applies to any file named REVIEW.md:
- Nobody may set `- Review status: APPROVED` while an item is PENDING or
  DEFERRED, or a CHANGED item is not `Verified: yes`.
- Subagents may only add items as PENDING. They may not change an existing
  item's Status or Verified field, and may never approve. Decisions are
  recorded by the main session, from the human's answers.
"""
import json
import os
import re
import sys

ITEM = re.compile(r"^## \[(\d+)/\d+\][^\n]*$", re.M)


def deny(msg: str) -> None:
    print(f"[review-gate] blocked: {msg}", file=sys.stderr)
    sys.exit(2)


def parse(text: str):
    """Return (approved, {item_no: {"status":..., "verified":...}})."""
    approved = bool(re.search(r"^- Review status:\s*APPROVED", text, re.M))
    items = {}
    heads = list(ITEM.finditer(text))
    for i, m in enumerate(heads):
        body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        st = re.search(r"^- Status:\s*(\w+)", body, re.M)
        ve = re.search(r"^- Verified:\s*([\w/]+)", body, re.M)
        items[m.group(1)] = {
            "status": st.group(1).upper() if st else "PENDING",
            "verified": ve.group(1).lower() if ve else "n/a",
        }
    return approved, items


def main() -> None:
    data = json.load(sys.stdin)
    tool = data.get("tool_name")
    inp = data.get("tool_input") or {}
    path = inp.get("file_path", "")
    if tool == "Bash":
        cmd = inp.get("command") or ""
        writes = r"(>|\btee\b|\bsed\s+(-\S*\s+)*-i|\bperl\s+(-\S*\s+)*-i|\bpython|\bmv\b|\bcp\b|\brm\b|\btruncate\b|\bdd\b|\bed\b|\bex\b)"
        if "REVIEW.md" in cmd and re.search(writes, cmd):
            deny("change REVIEW.md with the Edit or Write tool, so the approval gate can check it.")
        sys.exit(0)
    if tool not in ("Write", "Edit") or os.path.basename(path) != "REVIEW.md":
        sys.exit(0)

    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if tool == "Write":
        new = inp.get("content", "")
    else:
        o, n = inp.get("old_string", ""), inp.get("new_string", "")
        new = old.replace(o, n) if inp.get("replace_all") else old.replace(o, n, 1)

    old_ok, old_items = parse(old)
    new_ok, new_items = parse(new)
    agent = data.get("agent_type")

    if agent:
        if new_ok and not old_ok:
            deny(f"{agent} may not approve a review. Only the human approves, via the main session.")
        for k, v in new_items.items():
            prev = old_items.get(k)
            if prev is None and v["status"] != "PENDING":
                deny(f"{agent} may only add review items as PENDING (item {k}).")
            if prev is not None and v != prev:
                deny(f"{agent} may not change the decision fields of item {k}. Decisions come from the human.")

    if new_ok:
        blockers = []
        for k, v in sorted(new_items.items(), key=lambda kv: int(kv[0])):
            if v["status"] not in ("APPROVED", "CHANGED"):
                blockers.append(f"[{k}] {v['status']}")
            elif v["status"] == "CHANGED" and v["verified"] != "yes":
                blockers.append(f"[{k}] CHANGED, not verified")
        if not new_items:
            blockers.append("no items")
        if blockers:
            deny("cannot approve while items are open: " + ", ".join(blockers))
    sys.exit(0)


if __name__ == "__main__":
    main()
