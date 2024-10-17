__all__ = [
    "prolog_engine",
    "prt",
    "set_style",
    "get_main_value",
    "show_child_of_x",
    "START_COLOR",
    "CHILD_COLOR",
    "TITLE_COLOR",
    "ERROR_COLOR",
]

import re
from pyswip import Prolog

from src.env.ctypes import *
from src.env.logger import logger_handler, logging
from src.env.globales import *

prolog_engine = Prolog()

START_COLOR = "#fff7d1"
CHILD_COLOR = "#ffecc8"
TITLE_COLOR = "#ffd09b"
ERROR_COLOR = "#ffb0b0"


def prt(msg: str, level: int = logging.INFO) -> None:
    """
    Allows HTML. Inputs a message into the terminal and logs the raw message into the logger.
    """
    logger_handler.handler(level, msg, in_shell=True, raw_html=True, raw_msg=True)


def set_style(msg: str, hex_color: str = "#fff", extras: str = "") -> str:
    """
    Sets a default color to a string, ensuring other styled strings or messages won't break this.
    Handles opening and closing of extra tags properly.
    """

    # shoutout chatgpt because what the fuck
    def extract_closing_tags(extras: str) -> str:
        """
        Extracts closing tags from a given string of HTML-like tags, in reverse order.
        """
        # Find all opening tags using regex and close them in reverse order
        tags: List[Any] = re.findall(r"<([a-zA-Z][^>]*)>", extras)
        closing_tags: str = "".join(f"</{tag.split()[0]}>" for tag in reversed(tags))
        return closing_tags

    if extras:
        closing_tags: str = extract_closing_tags(extras)
        msg = f"{extras}{msg}{closing_tags}"

    return f'<style fg="{hex_color}">{msg}</style>'


def get_main_value() -> GenericSet:

    children = set()  # Use a set to avoid duplicates
    for result in prolog_engine.query(f"{PARENT}(_, X)"):
        children.add(result["X"])  # type: ignore[reportOptionalSubscript]
    return children


def show_child_of_x(x: LitStr, child_name: Dict[str, str]) -> None:
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
