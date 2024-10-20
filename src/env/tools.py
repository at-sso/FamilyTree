"""
GPL-3.0 License

Copyright (c) 2024 zperk
"""

__all__ = ["function_handler", "clear_terminal", "prt", "set_style"]

import os
import re
import traceback
from time import time as timer

from src.env.ctypes import *
from src.env.logger import *


def clear_terminal() -> int:
    """clears the terminal screen using platform-dependent commands."""
    return os.system("cls" if os.name == "nt" else "clear")


def function_handler(func: GenericCallable) -> Any:
    """Wraps a function call with logging and exception handling.

    This function takes another function (`func`) as an argument and executes it
    within a monitored context. Here's what happens:

    - Start Time Logging:
        - Captures the current time.
        - Logs a message using indicating the start of the wrapped function with its
          details obtained.

    - Function Execution:
        - Attempts to call the provided function `func` and stores the return value
          in `func_val`.

    - Exception Handling:
        - If an exception occurs during `func` execution:
            - Formats a final message using.
            - Logs a critical message using with details about the exception,
            including the function information and the traceback.
            - Calls `THE_MAIN_LOOP_WAS_TERMINATED`.
            - Re-raises the exception to propagate it further.

    - Normal Execution:
        - If no exception occurs:
            - Formats a final message.

    - Return Value:
        - Returns the value returned by the wrapped function.
    """
    start: float = timer()

    def __format_final_message(
        func: GenericCallable, is_exception: bool = False
    ) -> None:
        """
        The function `__format_final_message` logs the execution time of a given function based on the start and
        end timestamps.

        @param func The `func` parameter in the `__format_final_message` function is a callable that represents
        the function being executed. It can be any function that can be called with any number of arguments
        and returns a value of any type.
        """
        duration: float = start - timer()
        logger.debug(
            f"{'Unhandled operation' if is_exception else 'Operation'}: {func} took: {abs(duration)} ms."
        )

    logger.info(f"Start of: {func}.")

    try:
        func_val: Any = func()
    except Exception:
        __format_final_message(func, is_exception=True)
        logger.critical(
            f"Unhandled exception raised in {func}:" f"\n{traceback.format_exc()}"
        )
        raise

    __format_final_message(func)
    return func_val


def prt(msg: str, level: int = logging.INFO) -> None:
    """
    Accepts HTML input. Displays an HTML message in the terminal and logs its
    raw string representation to the logger.
    """
    logger_handler.handler(level, msg, in_shell=True, raw_msg=True)


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
        tags: list[Any] = re.findall(r"<([a-zA-Z][^>]*)>", extras)
        closing_tags: str = "".join(f"</{tag.split()[0]}>" for tag in reversed(tags))
        return closing_tags

    if extras:
        closing_tags: str = extract_closing_tags(extras)
        msg = f"{extras}{msg}{closing_tags}"

    return f'<style fg="{hex_color}">{msg}</style>'
