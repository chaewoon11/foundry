"""Shared helpers: find the project's foundry code folders and their settings.

Layout: <project>/foundry/<code>/foundry.json
  {"code": "<code>", "level": "L1|L2|L3", "source": ["path/to/main/code", ...]}
Workflow documents live under foundry/<code>/ (spec/, tests/, reference/, audit/, scripts/);
the main code stays where the project keeps it (the 'source' paths, relative to the project root).
"""
import json
import os

FOUNDRY_DIR = "foundry"


def project_root(data=None):
    return os.environ.get("CLAUDE_PROJECT_DIR") or (data or {}).get("cwd") or os.getcwd()


def codes(root):
    """List of dicts: name, dir (relative to root), level, source (list, relative to root)."""
    base = os.path.join(root, FOUNDRY_DIR)
    out = []
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        cfg = os.path.join(base, name, "foundry.json")
        if not os.path.isfile(cfg):
            continue
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
            "level": c.get("level") or "level not set",
            "source": [os.path.normpath(s) for s in src],
        })
    return out


def rel(path, root):
    """Path relative to root (normalised, symlinks resolved), or None if outside root."""
    p = os.path.realpath(path if os.path.isabs(path) else os.path.join(root, path))
    r = os.path.realpath(root)
    if p == r:
        return ""
    if p.startswith(r + os.sep):
        return os.path.relpath(p, r)
    return None


def under(relpath, d):
    d = d.rstrip("/")
    return d == "" or relpath == d or relpath.startswith(d + "/")


def expand(entries, code):
    """Code-relative policy entries -> project-relative paths for one code."""
    out = []
    for e in entries:
        if e == "@source":
            out.extend(code["source"])
        elif e == "progress":
            out.append(os.path.join(code["dir"], "progress"))
        else:
            out.append(os.path.join(code["dir"], e))
    return out
