# File: asm_tool/recon/subdomains.py

import shutil
import subprocess
import logging

logger = logging.getLogger("asm_tool.subdomains")

def enumerate_subdomains(domain: str) -> list[str]:
    """Use amass to enumerate subdomains, or skip if amass not installed."""
    if shutil.which("amass") is None:
        logger.warning("‘amass’ CLI not found on PATH; skipping subdomain enumeration.")
        return []

    try:
        result = subprocess.run(
            ["amass", "enum", "-d", domain, "-o", "-"],
            capture_output=True, text=True, check=True
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except subprocess.CalledProcessError as e:
        logger.error(f"Amass failed for {domain}: {e.stderr}")
        return []
