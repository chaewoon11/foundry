#!/usr/bin/env python3
"""foundry SessionStart hook: if the project has foundry runs, say so in one line per code."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from foundry_layout import codes, project_root  # noqa: E402

cs = codes(project_root())
if cs:
    lines = ["foundry runs in this project: " + ", ".join(c["name"] for c in cs) + "."]
    lines.append("To continue one or report where it stands, use the foundry:orchestrator skill "
                 "(it reads the run's state from foundry/<code>/).")
    missing = [c["name"] for c in cs if not c["configured"]]
    if missing:
        lines.append("No foundry.json (main-code paths) yet for: " + ", ".join(missing)
                     + " — the information barrier cannot protect the main code until it exists.")
    print("\n".join(lines))
