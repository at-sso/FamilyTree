"""
GNU GENERAL PUBLIC LICENSE

Copyright (c) 2024 zperk
"""

__all__ = ["logger"]

import os
import logging
from collections.abc import Callable
from prompt_toolkit import HTML, print_formatted_text
from typing import Any

from src.env.ctypes import *
from src.env.globales import *


class __LoggerHandler:
    def __init__(self) -> None:
        """
        The function initializes a logger with a specified log file and logs a message indicating the
        logger has started.
        """
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.__logger_function: Dict[int, Callable[[str], None]] = {
            logging.DEBUG: lambda x: self.logger.debug(x),
            logging.INFO: lambda x: self.logger.info(x),
            logging.WARNING: lambda x: self.logger.warning(x),
            logging.ERROR: lambda x: self.logger.error(x),
            logging.CRITICAL: lambda x: self.logger.critical(x),
        }

        self.logger.setLevel(logging.DEBUG)

        # Ensure the directory exists
        logger_directory: str = os.path.dirname(LOGGER_FILE)
        if not os.path.exists(logger_directory):
            os.makedirs(logger_directory)

        # Delete the oldest files.
        try:
            files: List[str] = os.listdir(LOGGER_FOLDER_PATH)
            if not len(files) < 10:
                logger_amount: int = max(len(files) // 10, 1)
                files_to_delete: List[str] = files[
                    : len(LOGGER_FOLDER_PATH) - logger_amount
                ]
                for file_name in files_to_delete:
                    file_path: str = os.path.join(LOGGER_FOLDER_PATH, file_name)
                    os.remove(file_path)
        # If `os.remove` fails, it's likely due to file permissions or non-existence.
        # Since file deletion is not essential for this operation, we can safely ignore exceptions.
        except:
            pass
        # Create a file handler
        logger_handler = logging.FileHandler(LOGGER_FILE, mode="w")
        # Create a formatter and set the formatter for the handler
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        logger_handler.setFormatter(formatter)
        # Add the handler to the logger
        self.logger.addHandler(logger_handler)

        self.handler(logging.INFO, "Logger started.")

    def handler(
        self,
        logging_level: int,
        message: Any,
        in_shell: bool = False,
        raw_msg: bool = False,
    ) -> None:
        """
        The function `__logger_message_handler` calls a specified function with a given argument.

        @param logging_level The level is expected to be an multiple of `10`, else raise a ValueError exception.
        @param msg Object that represents the message or information that will be passed
        to the `__logger_function` function for logging purposes.
        @param in_shell Forces the logger to print the `msg` parameter in the terminal. (optional)
        @param fg: Foreground color the `in_shell` message (optional).
        @param: raw_html: Set a raw HTML message and ignore anything else. Only works if `in_shell` is enabled. (optional)
        """
        if (logging_level % 10) != 0:
            raise ValueError(f"Logging level of {logging_level} is invalid.")
        if not self.logger.disabled:
            r: str = repr(message)
            if in_shell:
                try:
                    print_formatted_text(HTML(message))
                except:
                    print(r)
            self.__logger_function[logging_level](f"{r}" if raw_msg else message)


logger_handler = __LoggerHandler()


class __Logger:
    @staticmethod
    def debug(message: Any) -> None:
        """
        The function `debug` logs a debug message using a logger message handler.

        @param message The `message` parameter in the `debug` method is an object that represents the
        message to be logged at the 'DEBUG' level.
        """
        logger_handler.handler(logging.DEBUG, message)

    @staticmethod
    def info(message: Any) -> None:
        """
        This function logs an informational message using a logger message handler.

        @param message The `message` parameter in the `info` method is an object that represents the
        message to be logged at the 'INFO' level.
        """
        logger_handler.handler(logging.INFO, message)

    @staticmethod
    def warning(message: Any) -> None:
        """
        The `warning` function logs a warning message using a logger message handler.

        @param message The `message` parameter in the `info` warning is a string that represents the
        message to be logged at the 'WARNING' level.
        """
        logger_handler.handler(logging.WARNING, message)

    @staticmethod
    def error(message: Any) -> None:
        """
        The function `error` logs an error message using a logger message handler.

        @param message The `message` parameter in the `error` method is an object that represents the
        message to be logged at the 'ERROR' level.
        """
        logger_handler.handler(logging.ERROR, message)

    @staticmethod
    def critical(message: Any) -> None:
        """
        This function logs a critical message using a logger message handler.

        @param message The `message` parameter in the `critical` method is an object that represents the
        message to be logged at the 'CRITICAL' level.
        """
        logger_handler.handler(logging.CRITICAL, message)


logger = __Logger()
"""
This instance is used for logging messages at different levels such as debug, 
info, warning, error, and critical.
"""
