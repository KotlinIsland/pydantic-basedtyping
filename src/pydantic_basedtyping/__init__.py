"""implementation of the plugin."""

from __future__ import annotations

from basedtyping.transformer import EvalFailedError, _eval_direct  # noqa: PLC2701
from pydantic._internal import _typing_extra  # noqa: PLC2701
from pydantic.plugin import (
    PydanticPluginProtocol,
    ValidateJsonHandlerProtocol,
    ValidatePythonHandlerProtocol,
    ValidateStringsHandlerProtocol,
)
from pydantic_core import CoreConfig, CoreSchema
from typing_extensions import override


def _eval_type(
    value: object,
    globalns: dict[str, object] | None = None,
    localns: dict[str, object] | None = None,
    type_params: tuple[object, ...] | None = None,
) -> object:
    try:
        return _eval_direct(value, globalns, localns)
    except EvalFailedError as err:
        if hasattr(_typing_extra, "_eval_type_backport"):  # 2.9.2 has it
            return _typing_extra._eval_type_backport(  # type: ignore[no-any-expr] # noqa: SLF001
                err.ref,
                globalns,
                err.transformer.localns,
                # https://github.com/pydantic/pydantic/issues/10577
                type_params,  # type: ignore[arg-type]
            )
        raise


def _eval_type_lenient(
    value: object,
    globalns: dict[str, object] | None = None,
    localns: dict[str, object] | None = None,
) -> object:
    """Behaves like _typing_extra._eval_type_lenient, except it's based.

    Returns:
        the value of the type annotation
    """
    if value is None:
        value = _typing_extra.NoneType
    elif isinstance(value, str):
        value = _typing_extra._make_forward_ref(value, is_argument=False, is_class=True)  # noqa: SLF001

    try:
        return _eval_type(value, globalns, localns)
    except NameError:
        # the point of this function is to be tolerant to this case
        return value


_typing_extra.eval_type_lenient = _eval_type_lenient


class BasedtypingPlugin(PydanticPluginProtocol):
    """Support basedtyping functionality."""

    @override
    def new_schema_validator(
        self,
        schema: CoreSchema,
        schema_type: object,
        schema_type_path: object,
        schema_kind: object = None,
        config: CoreConfig | None = None,
        plugin_settings: dict[str, object] | None = None,
    ) -> (
        ValidatePythonHandlerProtocol | None,
        ValidateJsonHandlerProtocol | None,
        ValidateStringsHandlerProtocol | None,
    ):
        return None, None, None


plugin = BasedtypingPlugin()
