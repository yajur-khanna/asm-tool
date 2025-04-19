import requests

def filter_live(subdomains: list[str]) -> list[str]:
    """Check which subdomains respond over HTTP/S."""
    live: list[str] = []
    for sub in subdomains:
        for scheme in ("http://", "https://"):
            try:
                resp = requests.get(scheme + sub, timeout=5)
                if resp.status_code < 400:
                    live.append(sub)
                    break
            except requests.RequestException:
                continue
    return live
