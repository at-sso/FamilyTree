from collections.abc import (
    Callable,
)
from typing import (
    Any,
    Generic,
    TypeVar,
)
from typing_extensions import (
    ParamSpec,
    LiteralString,
)

List = list
Dict = dict
Tuple = tuple
Type = type
LitStr = LiteralString

# Type constructors:
_P = ParamSpec("_P")
_R = TypeVar("_R", bound=Any)


class CallableConstructor(Generic[_P, _R]):
    def __init__(self, func: Callable[_P, _R]) -> None:
        self.func = func

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _R:
        return self.func(*args, **kwargs)


# Callables
GenericCallable = Callable[..., Any]

# Lists
GenericList = List[Any]
StrList = List[str]

# Maps
GenericMap = Dict[Any, Any]

# Sets:
GenericSet = set[Any]
StringSet = set[str]
