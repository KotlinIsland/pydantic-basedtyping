import contextlib
import importlib
import sys
from io import StringIO
from pathlib import Path

from _pytest._py.path import LocalPath
from mypy.util import safe
from pytest import MonkeyPatch

from pydantic_basedtyping import __main__


def test_install(tmpdir: LocalPath, monkeypatch: MonkeyPatch):
    location: LocalPath = tmpdir.join("site-packages").mkdir()  # type: ignore[arg-type, no-untyped-call] # it's typed wrong
    monkeypatch.syspath_prepend(location)  # type: ignore[no-untyped-call]
    # too hard to test the case where it doesn't exist in the first place
    #  because we need to import things from `site-packages`
    sitecustomize_file = location.join("sitecustomize.py")  # type: ignore[arg-type] # it's typed wrong
    sitecustomize_file.write("")  # type: ignore[no-untyped-call]
    sys.modules.pop("sitecustomize", None)

    with contextlib.redirect_stdout(StringIO()) as stdout:
        assert __main__.install() == 0
    assert stdout.getvalue() == f"installing to {sitecustomize_file}\n"

    sitecustomize = importlib.import_module("sitecustomize")

    assert __main__.install_code in Path(safe(sitecustomize.__file__)).read_text(
        encoding="utf-8"
    )

    with contextlib.redirect_stdout(StringIO()) as stdout:
        assert __main__.install() == 0
    assert stdout.getvalue() == "looks like it's already installed :)\n"
