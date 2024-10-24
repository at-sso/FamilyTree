"""
MIT License

Copyright (c) 2024 zperk
"""

__all__ = [
    "prolog_engine",
    "get_main_value",
    "x_of_child",
    "START_COLOR",
    "CHILD_COLOR",
    "PARENT_COLOR",
    "ERROR_COLOR",
]


from pyswip import Prolog

from src.env.ctypes import *
from src.env.globales import *
from src.env import tools

prolog_engine = Prolog()

START_COLOR = "#fff7d1"
CHILD_COLOR = "#ffecc8"
PARENT_COLOR = "#ffd09b"
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


def x_of_child(x: LitStr, child_name: dict[str, str]) -> None:
    """
    Shows the child of a given value (x).

    Args:
        x: The value to query for.
        child_name: A dictionary containing the HTML and raw string representations of the child name.
        The keys of this dictionary must be 'str' and 'html'.
    """
    child_name_str = child_name["str"]
    child_name_html = child_name["html"]

    # Format the title of "x" (e.g. {x = Parent} of {child_name = Any}).
    capital_x_title: str = tools.set_style(x.capitalize(), PARENT_COLOR, "<b><i>")
    tools.prt(f"\n{capital_x_title} of {child_name_html}:")

    # Query for relationships
    results: StrList = list(
        prolog_engine.query(
            f"{x}(X, {child_name_str.lower()})"  # type:ignore[reportUnknownArgumentType]
        )
    )

    if results:  # If there's any results,
        # Format and show the results.
        for result in results:
            r: str = result["X"]  # type: ignore[reportArgumentType]
            tools.prt(
                f"{tools.set_style(r.capitalize(), CHILD_COLOR, '<b><i>')} "  # type: ignore[reportUnknownArgumentType]
                f"is the {x} of {child_name_html}"
            )
    else:  # Inform the user that the child doesn't have any 'x' (any parents)
        tools.prt(
            tools.set_style(
                f"{child_name_html} does not have any {x}(s).", ERROR_COLOR, "<i>"
            )
        )
