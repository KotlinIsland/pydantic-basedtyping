import contextlib
import importlib
import sys
from io import StringIO
from pathlib import Path

from mypy.util import safe
from pytest import MonkeyPatch

from pydantic_basedtyping import __main__


def test_install(tmp_path: Path, monkeypatch: MonkeyPatch):
    location = tmp_path / "site-packages"
    location.mkdir()
    monkeypatch.syspath_prepend(location)  # type: ignore[no-untyped-call]
    # too hard to test the case where it doesn't exist in the first place
    #  because we need to import things from `site-packages`
    sitecustomize_file = location / "sitecustomize.py"
    sitecustomize_file.touch()
    sys.modules.pop("sitecustomize", None)

    with contextlib.redirect_stdout(StringIO()) as stdout:
        assert __main__.install() == 0
    assert stdout.getvalue() == f"installing to {sitecustomize_file}\n"

    sitecustomize = importlib.import_module("sitecustomize")

    assert __main__.install_code in Path(safe(sitecustomize.__file__)).read_text()

    with contextlib.redirect_stdout(StringIO()) as stdout:
        assert __main__.install() == 0
    assert stdout.getvalue() == "looks like it's already installed :)\n"
