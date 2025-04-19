# File: asm_tool/utils.py

import logging
import subprocess
from typing import List, Dict, Any

def init_logger(name: str = "asm_tool", level: str = "INFO") -> logging.Logger:
    """
    Initialize and return a logger with a console handler.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger


def run_subprocess(
    cmd: List[str],
    capture_output: bool = True,
    text: bool = True,
    check: bool = True,
    **kwargs: Any
) -> subprocess.CompletedProcess:
    """
    Wrap subprocess.run to execute external commands and log on errors.
    Returns the CompletedProcess on success, or re‑raises on failure.
    """
    logger = logging.getLogger("asm_tool.subprocess")
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=text,
            check=check,
            **kwargs
        )
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command `{cmd}` failed (exit {e.returncode}): {e.stderr}")
        raise
