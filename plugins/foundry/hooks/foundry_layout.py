"""Shared helpers: find the project's foundry code folders and their settings.

Layout: <project>/foundry/<code>/foundry.json  {"code": "<code>", "source": ["path/to/main/code", ...]}
Workflow documents live under foundry/<code>/; the main code stays where the
project keeps it ('source' paths, relative to the project root).
"""
import json
import os

FOUNDRY_DIR = "foundry"


def project_root(data=None):
    return os.environ.get("CLAUDE_PROJECT_DIR") or (data or {}).get("cwd") or os.getcwd()


def codes(root):
    """Dicts with name, dir (relative to root) and source (list, relative to root)."""
    base = os.path.join(root, FOUNDRY_DIR)
    out = []
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        d = os.path.join(base, name)
        if not os.path.isdir(d) or name.startswith("."):
            continue
        cfg = os.path.join(d, "foundry.json")
        c = {}
        if os.path.isfile(cfg):
            try:
                with open(cfg, encoding="utf-8") as f:
                    c = json.load(f)
            except (OSError, ValueError):
                c = {}
        src = c.get("source") or []
        if isinstance(src, str):
            src = [src]
        out.append({
            "name": name,
            "dir": os.path.join(FOUNDRY_DIR, name),
            "source": [os.path.normpath(s) for s in src if s],
            "configured": os.path.isfile(cfg),
        })
    return out


def rel(path, root):
    """Path relative to root (normalised, symlinks resolved), or None if outside root."""
    if not path:
        return None
    p = os.path.realpath(path if os.path.isabs(path) else os.path.join(root, path))
    r = os.path.realpath(root)
    if p == r:
        return ""
    if p.startswith(r + os.sep):
        return os.path.relpath(p, r)
    return None


def _segments(p):
    return [s for s in p.strip("/").split("/") if s not in ("", ".")]


def under(relpath, pattern):
    """True if relpath is pattern or inside it; '*' in pattern matches one segment."""
    ps, rs = _segments(pattern), _segments(relpath)
    if not ps:
        return True
    if len(rs) < len(ps):
        return False
    return all(a == "*" or a == b for a, b in zip(ps, rs))


def contains(relpath, pattern):
    """True if the directory relpath contains (part of) pattern."""
    ps, rs = _segments(pattern), _segments(relpath)
    if len(rs) >= len(ps):
        return False
    return all(a == "*" or a == b for a, b in zip(ps, rs))


def expand(entries, code):
    """Code-relative policy entries -> project-relative patterns for one code."""
    out = []
    for e in entries:
        if e == "@source":
            out.extend(code["source"])
        else:
            out.append(os.path.join(code["dir"], e))
    return out
