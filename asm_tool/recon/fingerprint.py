from Wappalyzer import Wappalyzer, WebPage

wappalyzer = Wappalyzer.latest()

def detect_technologies(url: str) -> list[str]:
    """Fingerprint technologies used by the site."""
    webpage = WebPage.new_from_url(url)
    techs = wappalyzer.analyze(webpage)
    return list(techs.keys())


# File: asm_tool/recon/ssl_analysis.py
import subprocess
import json

def analyze_ssl(domain: str) -> dict:
    """Run SSLyze to analyze SSL/TLS configuration."""
    try:
        result = subprocess.run(
            ["sslyze", "--json_out=-", domain],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except Exception:
        return {}
