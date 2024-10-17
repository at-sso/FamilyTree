"""
MIT License

Copyright (c) 2024 zperk
"""

__all__ = [
    "prolog_engine",
    "get_main_value",
    "show_child_of_x",
    "START_COLOR",
    "CHILD_COLOR",
    "TITLE_COLOR",
    "ERROR_COLOR",
]


from pyswip import Prolog

from src.env.ctypes import *
from src.env.globales import *
from src.env.tools import *

prolog_engine = Prolog()

START_COLOR = "#fff7d1"
CHILD_COLOR = "#ffecc8"
TITLE_COLOR = "#ffd09b"
ERROR_COLOR = "#ffb0b0"


def get_main_value() -> GenericSet:
    """
    Queries the Prolog engine for all values that have a parent.

    Returns:
        A set of values that have a parent.
    """
    children = set()  # Use a set to avoid duplicates
    for result in prolog_engine.query(f"{PARENT}(_, X)"):
        children.add(result["X"])  # type: ignore[reportOptionalSubscript]
    return children


def show_child_of_x(x: LitStr, child_name: Dict[str, str]) -> None:
    """
    Shows the child of a given value.

    Args:
        x: The value to query for.
        child_name: A dictionary containing the HTML and raw string representations of the child name.
    """
    capital_x: str = set_style(x.capitalize(), TITLE_COLOR, "<b><i>")

    prt(f"\n{capital_x} of {child_name['html']}:")

    # Query for relationships
    results: StrList | Any = list(
        prolog_engine.query(f"{x}(X, {child_name['str'].lower()})")
    )

    if results:
        for result in results:
            r: str = result["X"]  # type: ignore[reportArgumentType]
            prt(
                f"{set_style(r.capitalize(), CHILD_COLOR, '<b><i>')} "  # type: ignore[reportUnknownArgumentType]
                f"is the {x} of {child_name['html']}"
            )
    else:
        # If no results, inform the user that the child doesn't have any 'x'
        prt(f"{child_name['html']} doesn't have any {x}.")
