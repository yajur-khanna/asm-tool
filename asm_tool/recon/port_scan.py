# File: asm_tool/recon/port_scan.py

import shutil
import logging
from asm_tool.utils import run_subprocess

logger = logging.getLogger("asm_tool.port_scan")

def scan_ports(domain: str, ports: str = None) -> list[dict]:
    """
    Perform a fast Nmap scan (top ports) or skip if nmap not installed.
    """
    if shutil.which("nmap") is None:
        logger.warning("‘nmap’ CLI not found; skipping port scan.")
        return []

    try:
        # Quick scan of default top 100 ports
        args = ["nmap", "-sV", "-T4", "-F", domain]
        run_subprocess(args)

        # Now parse results with python‑nmap (top ports only)
        import nmap
        nm = nmap.PortScanner()
        nm.scan(domain, arguments="-sV -T4 -F")
        results = []
        if domain in nm.all_hosts():
            for proto in nm[domain].all_protocols():
                for port in nm[domain][proto]:
                    info = nm[domain][proto][port]
                    results.append({
                        "port":    port,
                        "state":   info.get("state"),
                        "service": info.get("name"),
                        "version": info.get("version", ""),
                    })
        return results

    except Exception as e:
        logger.error(f"Port scan failed for {domain}: {e}")
        return []
