import requests
from asm_tool.config import HAVEIBEENPWNED_API_KEY

def check_breach(account: str) -> list[dict]:
    """Check HaveIBeenPwned for breaches."""
    headers = {"hibp-api-key": HAVEIBEENPWNED_API_KEY}
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{account}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []