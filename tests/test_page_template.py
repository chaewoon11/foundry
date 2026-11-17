"""Briefing page template (skills/brief/page-template.html)."""
import os
import re

from conftest import PLUGIN

PAGE = os.path.join(PLUGIN, "skills", "brief", "page-template.html")


def test_page_template_contract():
    t = open(PAGE, encoding="utf-8").read()
    assert re.search(r"cdnjs\.cloudflare\.com/ajax/libs/mathjax/\d+\.\d+\.\d+/es5/tex-svg", t)  # pinned MathJax
    assert "prefers-color-scheme: dark" in t and ':root[data-theme="dark"]' in t                 # both themes
    assert 'name="viewport"' in t
    for sid in ["conventions", "problem", "algorithm", "structure", "verification", "scope", "decisions"]:
        assert f'id="{sid}"' in t, sid
    assert t.count('class="takeaway"') >= 7
