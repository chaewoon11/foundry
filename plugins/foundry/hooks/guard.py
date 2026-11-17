#!/usr/bin/env python3
"""foundry information barrier (PreToolUse hook).

Identifies the calling workflow agent from `agent_type` (plugin agents arrive as
`foundry:<role>`; the prefix is stripped) and allows or blocks Read / Write /
Edit / NotebookEdit / Glob / Grep / Bash according to policy.json, applied to
every code folder under <project>/foundry/. Blocks exit with code 2 and a reason
on stderr. The main session and non-workflow agents are not restricted; with no
foundry/ folder in the project nothing is restricted.

Limits: Bash is checked by its command string only. The developer gets an
allowlist; other roles get a forbidden-path check, which a determined agent
could bypass.
"""
import json
import os
import re
import shlex
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from foundry_layout import codes, expand, project_root, rel, under  # noqa: E402

SAFE_ARGS = r"(\s[^;&|<>`$\\]*)?$"


def deny(msg):
    print(f"[foundry guard] blocked: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    data = json.load(sys.stdin)
    agent = (data.get("agent_type") or "").split(":")[-1]
    if not agent:
        sys.exit(0)
    with open(os.path.join(HERE, "policy.json"), encoding="utf-8") as f:
        policy = json.load(f)
    role = policy["roles"].get(agent)
    if role is None:
        sys.exit(0)

    root = project_root(data)
    cs = codes(root)
    if not cs:
        sys.exit(0)

    read_deny, write_allow, create_only, protected = [], [], [], []
    for c in cs:
        read_deny += expand(role.get("read_deny", []), c)
        write_allow += expand(role.get("write_allow", []), c)
        create_only += expand(role.get("create_only", []), c)
        protected += expand(policy.get("protected", []), c)
    sources = [s for c in cs for s in c["source"]]

    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    cwd = data.get("cwd") or root

    def check_read(path):
        r = rel(path, root)
        if r is None:
            return
        for d in read_deny:
            if under(r, d):
                deny(f"{agent} may not read {d}/ ({r}).")

    def check_search(base, *patterns):
        r = rel(base or cwd, root)
        if r is not None:
            for d in read_deny:
                if under(r, d):
                    deny(f"{agent} may not search {d}/.")
                if under(d, r):
                    deny(f"search scope '{r or 'project root'}' contains forbidden path {d}/; "
                         "pass an allowed subdirectory as `path`.")
        for pat in patterns:
            if pat and any(d in pat for d in read_deny):
                deny(f"search pattern references a forbidden path: {pat}")

    def check_write(path):
        r = rel(path, root)
        if r is None:
            deny(f"{agent} may not write outside the project ({path}).")
        for d in read_deny + protected:
            if under(r, d):
                deny(f"{agent} may not write {r}.")
        if any(under(r, d) for d in write_allow):
            return
        for d in create_only:
            if under(r, d):
                if tool == "Write" and not os.path.exists(os.path.join(root, r)):
                    return
                deny(f"{agent} may only create new files in {d}/ (cannot modify {r}).")
        allowed = ", ".join(f"{d}/" for d in write_allow + create_only) or "(none)"
        deny(f"{agent} may not write {r}. Writable: {allowed}")

    def check_bash_developer(cmd):
        scripts = r"^(\./)?foundry/[A-Za-z0-9_.-]+/scripts/(build|run-public-tests)" + SAFE_ARGS
        if re.match(scripts, cmd) and ".." not in cmd:
            return
        if re.match(r"^git status( --short| -s)?$", cmd) or re.match(r"^git log --oneline( -n [0-9]+)?$", cmd):
            return
        m = re.match(r"^git diff( --stat)? -- (.+)$", cmd)
        if m and not re.search(r"[;&|<>`$\\]|\.\.", cmd):
            try:
                paths = shlex.split(m.group(2))
            except ValueError:
                paths = []
            if paths and all(any(under(os.path.normpath(p), s) for s in sources) for p in paths):
                return
        deny(f"{agent} may only run: foundry/<code>/scripts/build, foundry/<code>/scripts/run-public-tests "
             "(plain arguments), git status, git log --oneline [-n N], git diff [--stat] -- <main-code paths>. "
             "No chaining, pipes, redirects or substitutions.")

    def check_bash_other(cmd):
        for d in read_deny:
            tails = {d}
            for c in cs:
                if d.startswith(c["dir"] + "/"):
                    tails.add(d[len(c["dir"]) + 1:])
            for t in tails:
                if re.search(rf"(^|[\s'\"=/.]){re.escape(t)}(/|\b)", cmd):
                    deny(f"{agent}'s command references forbidden path {d}/.")

    if tool == "Read":
        check_read(inp.get("file_path", ""))
    elif tool in ("Write", "Edit"):
        check_write(inp.get("file_path", ""))
    elif tool == "NotebookEdit":
        check_write(inp.get("notebook_path", ""))
    elif tool == "Glob":
        check_search(inp.get("path"), inp.get("pattern"))
    elif tool == "Grep":
        check_search(inp.get("path"), inp.get("glob"))
    elif tool == "Bash":
        cmd = (inp.get("command") or "").strip()
        if role.get("bash") == "developer":
            check_bash_developer(cmd)
        else:
            check_bash_other(cmd)
    sys.exit(0)


if __name__ == "__main__":
    main()
