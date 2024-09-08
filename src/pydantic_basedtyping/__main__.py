"""cli interface for `pydantic-basedtyping`.

```console
> python -m pydantic_basedtyping install
```
"""

import sys
from pathlib import Path
from types import ModuleType
from typing import cast

# language=python  # noqa: ERA001
install_code = """
# activate pydantic-basedtyping
import pydantic_basedtyping
"""


def install() -> int:
    """Install pydantic-basedtyping.

    Returns:
        exit code

    Raises:
         AssertionError: if the sitecustomize module does not have a file path
    """
    echo = print  # hide print from ruff
    try:
        import sitecustomize  # type: ignore[import-not-found, import-untyped, unused-ignore] # noqa: PLC0415
    except ImportError:
        paths = [Path(p) for p in sys.path]
        try:
            path = next(p for p in paths if p.is_dir() and p.name == "site-packages")
        except StopIteration:
            echo(
                "unable to file a suitable path to save `sitecustomize.py`"
                f" to from sys.path: {paths}"
            )
            return 1
        else:
            install_path = path / "sitecustomize.py"
    except Exception as e:  # noqa: BLE001
        sys.exit(f"unexpected exception while loading `sitecustomize.py`.:\n  {e}")
    else:
        file = cast(ModuleType, sitecustomize).__file__
        if not file:
            msg = "'sitecustomize' module did not have a file path"
            raise AssertionError(msg)
        install_path = Path(file)

    if install_path.exists() and install_code in install_path.read_text():
        echo("looks like it's already installed :)")
        return 0

    echo(f"installing to {install_path}")
    with install_path.open("a") as f:
        f.write(install_code)
    return 0


if __name__ == "__main__":
    if "install" in sys.argv:
        sys.exit(install())
