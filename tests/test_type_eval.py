from __future__ import annotations

import re
import sys
from typing import Union

import pytest
from pydantic import BaseModel, ValidationError
from pydantic._internal import _typing_extra  # noqa: PLC2701


def test_simple():
    class _A(BaseModel):
        a: Union[1, 2]  # noqa: UP007 using `Union` for 3.9 support

    _A(a=1)
    _A(a=2)
    with pytest.raises(ValidationError):
        _A(a=3)  # type: ignore[arg-type]


@pytest.mark.skipif(sys.version_info >= (3, 10), reason="only needed for 3.9")
def test_backport():
    if hasattr(_typing_extra, "_eval_type_backport"):
        expected = re.compile(
            "Unable to evaluate type annotation .* "
            "If you are making use of the new typing syntax .* "
            "`eval_type_backport`"
        )
    else:
        expected = re.compile(r"\(\"unsupported operand type\(s\) for \|: '")
    with pytest.raises(
        TypeError,
        match=expected,
    ):

        class _A(BaseModel):
            a: 1 | 2
