# pydantic-basedtyping

support for basedtyping features with pydantic:

```py
from __future__ import annotations

from pydantic import BaseModel

class A(BaseModel):
    a: 1 | 2
A(a=1)  # A(a=1)
A(a=2)  # A(a=2)
A(a=3)  # ValidationError
```

> [!NOTE]
> the types need to be written as a string, or `__future__.annotations` needs to be enabled

# installation

1. add `pydantic-basedtyping` as a dependency
2. install the plugin with:
    ```console
    python -m pydantic_basedtyping install
    ```

if you are using [pyprojectx](https://pyprojectx.github.io/), this can be configured:
```toml
[tool.pyprojectx]
install = ["uv sync", "uv run python -m pydantic_basedtyping install"]
```
