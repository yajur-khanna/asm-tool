# File: asm_tool/output.py

import os
import json
from datetime import datetime
from asm_tool.utils import init_logger

# Initialize logger for this module
logger = init_logger(__name__)

def write_json_report(domain: str, report: dict, out_dir: str = "reports") -> None:
    """
    Write the scan report as JSON to reports/{domain}_{timestamp}.json
    """
    # Ensure output directory exists
    os.makedirs(out_dir, exist_ok=True)

    # Construct filename with UTC timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe_domain = domain.replace(".", "_")
    filename = f"{safe_domain}_{timestamp}.json"
    path = os.path.join(out_dir, filename)

    # Dump JSON
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        logger.info(f"Wrote JSON report for {domain} → {path}")
    except Exception as e:
        logger.error(f"Failed to write report for {domain}: {e}")
