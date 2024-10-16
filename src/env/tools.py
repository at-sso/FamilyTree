__all__ = ["function_handler", "clear_terminal"]

import os
from time import time as timer
import traceback

from .ctypes import *
from .logger import *


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
            f"{'Unhandled operation' if is_exception else 'Operation'}: "
            f"{func} took: {abs(duration if duration > 0.0 else 0.0)} ms."
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
