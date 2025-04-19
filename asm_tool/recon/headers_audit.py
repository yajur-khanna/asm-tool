import requests

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "X-Frame-Options",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "Referrer-Policy",
]

def audit_headers(domain: str) -> dict:
    """Check for presence of key HTTP security headers."""
    try:
        resp = requests.get(f"https://{domain}", timeout=5)
        return {h: resp.headers.get(h) for h in SECURITY_HEADERS}
    except requests.RequestException:
        return {}