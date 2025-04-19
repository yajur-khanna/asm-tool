import dns.resolver
import whois

def get_dns_records(domain: str) -> dict:
    records: dict = {}
    for rtype in ["A", "AAAA", "MX", "TXT", "NS"]:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [str(rdata) for rdata in answers]
        except Exception:
            records[rtype] = []
    return records


def get_whois_info(domain: str) -> dict:
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
        }
    except Exception:
        return {}