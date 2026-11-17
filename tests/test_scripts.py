"""Script templates (templates/scripts) end to end on a tiny Python project."""
import os
import subprocess
import textwrap

import pytest

from conftest import init, run

META = 'import pytest\n'


@pytest.fixture
def toy(project):
    init(project, "toy", "pkg", level="L3")
    (project / "pkg" / "toy").mkdir(parents=True)
    (project / "pkg/toy/__init__.py").write_text("def double(x):\n    return 2 * x\n")
    cd = project / "foundry/toy"
    (cd / "tests/conftest.py").write_text(
        "def pytest_configure(config):\n    config.addinivalue_line('markers', 'meta(**kw): metadata')\n")
    (cd / "tests/public/test_pub.py").write_text(textwrap.dedent("""
        import pytest
        @pytest.mark.meta(kind=1)
        def test_double():
            from toy import double
            assert double(3) == 6
    """))
    (cd / "tests/holdout/test_hold.py").write_text(textwrap.dedent("""
        import pytest
        @pytest.mark.meta(kind=2)
        def test_linear():
            from toy import double
            assert double(5) - double(2) == double(3)
        @pytest.mark.meta(kind=1)
        def test_secret_value_12345():
            from toy import double
            assert double(7) == 14
    """))
    build = cd / "scripts/build"
    build.write_text(build.read_text().replace("import sys; print('build: ok')", "import toy; print('build: ok')"))
    return project


def sh(project, *args, **kw):
    return run([str(project / "foundry/toy/scripts" / args[0]), *args[1:]], project, **kw)


def patch_file(project, name, old, new):
    p = project / "patch" / f"{name}.patch"
    p.parent.mkdir(exist_ok=True)
    src = (project / "pkg/toy/__init__.py").read_text().splitlines(True)
    import difflib
    dst = [l.replace(old, new) for l in src]
    p.write_text("".join(difflib.unified_diff(src, dst, "a/pkg/toy/__init__.py", "b/pkg/toy/__init__.py")))
    return str(p)


def test_build_and_public(toy):
    assert "build: ok" in sh(toy, "build").stdout
    r = sh(toy, "run-public-tests", "-q")
    assert r.returncode == 0 and "1 passed" in r.stdout


def test_holdout_prints_counts_only(toy):
    r = sh(toy, "run-holdout")
    assert r.returncode == 0
    assert "kind=1 pass=1 fail=0" in r.stdout and "kind=2 pass=1 fail=0" in r.stdout
    assert "secret" not in r.stdout and "test_" not in r.stdout
    assert (toy / "foundry/toy/audit/private/holdout.log").is_file()


def test_mutate(toy):
    assert "baseline PASS" in sh(toy, "mutate", "--baseline").stdout
    assert sh(toy, "mutate", patch_file(toy, "kill", "2 * x", "3 * x")).stdout.strip() == "kill KILLED"
    assert sh(toy, "mutate", patch_file(toy, "same", "2 * x", "x + x")).stdout.strip() == "same SURVIVED"
    bad = toy / "patch/bad.patch"; bad.write_text("garbage\n")
    assert sh(toy, "mutate", str(bad), "--id", "B").stdout.strip() == "B INVALID"
    assert (toy / "pkg/toy/__init__.py").read_text() == "def double(x):\n    return 2 * x\n"  # original untouched
