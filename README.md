# pydantic-basedtyping

support for basedtyping features with pydantic:

```py
from pydantic import BaseModel

class A(BaseModel):
    a: 1 | 2
A(a=1)  # A(a=1)
A(a=2)  # A(a=2)
A(a=3)  # ValidationError
```

# installation

1. add `pydantic-basedtyping` as a dependency
2. install the plugin with:
    ```console
    python -m pydantic_basedtyping install
    ```

this can be configured with pyprojectx:
```toml
[tool.pyprojectx]
install = "uv sync; uv run python -m pydantic_basedtyping install"
```
