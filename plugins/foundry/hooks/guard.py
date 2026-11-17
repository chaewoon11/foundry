#!/usr/bin/env python3
"""foundry information barrier (PreToolUse hook).

Identifies the calling agent from `agent_type` (plugin agents arrive as
`foundry:<name>`) and allows or blocks Read / Write / Edit / NotebookEdit /
Glob / Grep / Bash according to policy.json, for every code folder under
<project>/foundry/. A block exits with code 2 and the reason on stderr.
The main session and other agents are not restricted; with no foundry/
folder nothing is restricted.

Limits: Bash is checked by its command string only. It stops an agent from
wandering into a forbidden file, not a determined attempt to get around it.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from foundry_layout import codes, contains, expand, project_root, rel, under  # noqa: E402

READERS = r"(cat|less|more|head|tail|nl|sed|awk|grep|egrep|rg|ag|strings|xxd|od|hexdump|diff|cmp|cp|mv|rsync|tar|zip|vi|vim|nano|emacs|code|open|base64|sort|uniq|wc|tee|file|ls|tree|find|git)"
# The developer may not search the project recursively or read git history/objects:
# holdout tests are committed, so history would show them.
DEV_DENY = [
    (r"\bgit\s+(log\s.*(-p|--patch|--stat|-S|-G)|show|grep|cat-file|archive|blame|checkout|restore|stash\s+show|diff\s.*(HEAD|\.\.|[0-9a-f]{7,}|--cached|--staged))", "git history and objects"),
    (r"\b(grep|egrep|rg|ag)\b[^|;&]*\s-[a-zA-Z]*[rR]", "recursive search (use the Grep tool with an allowed path)"),
    (r"\b(rg|ag)\b", "recursive search (use the Grep tool with an allowed path)"),
    (r"\b(find|tree)\b|\bls\b[^|;&]*\s-[a-zA-Z]*R", "listing the project recursively (use the Glob tool)"),
    (r"foundry/[^\s'\"]*[*?\[]", "wildcards in foundry/ paths"),
    (r"(^|\s|/)\.\.(/|\s|$)", "'..' in paths"),
]


def deny(msg):
    print(f"[foundry guard] blocked: {msg}", file=sys.stderr)
    sys.exit(2)


def path_regex(pattern):
    """Regex matching a project-relative pattern (or its tail after foundry/<code>/) in a command."""
    parts = [re.escape(s) if s != "*" else r"[^/\s'\"]+" for s in pattern.strip("/").split("/")]
    return "/".join(parts)


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

    read_deny, write_allow, create_only, protected, sources = [], [], [], [], []
    for c in cs:
        read_deny += expand(role.get("read_deny", []), c)
        write_allow += expand(role.get("write_allow", []), c)
        create_only += expand(role.get("create_only", []), c)
        protected += expand(policy.get("protected", []), c)
        if "@source" in role.get("read_deny", []):
            sources += c["source"]

    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    cwd = data.get("cwd") or root

    def check_read(path):
        r = rel(path, root)
        if r is None:
            return
        for d in read_deny:
            if under(r, d):
                deny(f"{agent} may not read {d} ({r}).")

    def check_search(base, *patterns):
        r = rel(base or cwd, root)
        if r is not None:
            for d in read_deny:
                if under(r, d):
                    deny(f"{agent} may not search {d}.")
                if contains(r, d):
                    deny(f"search scope '{r or 'project root'}' contains {d}, which {agent} may not see; "
                         "pass a narrower `path`.")
        for pat in patterns:
            for d in read_deny:
                if pat and re.search(path_regex(d), pat):
                    deny(f"search pattern points at {d}.")

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
                deny(f"{agent} may only create new files in {d} (cannot modify {r}).")
        allowed = ", ".join(write_allow + create_only) or "(nothing)"
        deny(f"{agent} may not write {r}. Writable: {allowed}")

    def check_bash(cmd):
        if role.get("bash") == "developer":
            for rx, what in DEV_DENY:
                if re.search(rx, cmd):
                    deny(f"{agent} may not use {what}.")
        for d in read_deny:
            tails = {d}
            for c in cs:
                if d.startswith(c["dir"] + "/"):
                    tails.add(d[len(c["dir"]) + 1:])
            for t in tails:
                if not re.search(rf"(^|[\s'\"=/:]){path_regex(t)}(/|\b|$)", cmd):
                    continue
                # Main code may be run (e.g. existing code by the test designer), not read.
                if d in sources and not re.search(rf"(^|[\s;&|(]){READERS}\b", cmd) \
                        and not re.search(r"open\(|read_text|readlines|import\s+inspect|getsource", cmd):
                    continue
                deny(f"{agent}'s command touches {d}, which it may not see.")

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
        check_bash((inp.get("command") or "").strip())
    sys.exit(0)


if __name__ == "__main__":
    main()
