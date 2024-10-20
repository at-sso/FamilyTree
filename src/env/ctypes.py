"""
GPL-3.0 License

Copyright (c) 2024 zperk
"""

from collections.abc import Callable
from typing import Any
from typing_extensions import LiteralString

LitStr = LiteralString

# Callables
GenericCallable = Callable[..., Any]

# Lists
StrList = list[str]

# Sets:
GenericSet = set[Any]
StringSet = set[str]
