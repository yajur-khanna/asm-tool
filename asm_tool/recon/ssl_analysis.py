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