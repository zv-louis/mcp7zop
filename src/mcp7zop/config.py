# encoding : utf-8

import os
import sys
import logging
from pathlib import Path

config = {}
logger_instance = None

# get_config function to load configuration settings
def get_config() -> dict[str, str]:
        """
        get_config function to load configuration settings.
        """
        if not config:
            # load from ${_HOME}/.mcp7zop/config.json
            home = os.path.expanduser("~")
            config_path = Path(home) / ".mcp7zop" / "config.json"
            if config_path.exists():
                import json
                with open(config_path, 'r') as f:
                    config.update(json.load(f))
        return config

def get_logger() -> logging.Logger:
    """
    Get a logger with the specified name.
    """
    if logger_instance is None:
        # Set up the logger
        stderr_handler = logging.StreamHandler(stream=sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        # stderr_handler.addFilter(lambda record: record.levelno <= logging.INFO)
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        stderr_handler.setFormatter(formatter)

        # ロガーにハンドラを設定する
        logger_instance = logging.getLogger("mcp7zop")
        logger_instance.setLevel(logging.WARNING)
        logger_instance.addHandler(stderr_handler)

    return logger_instance
