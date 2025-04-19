import csv

def load_domains(csv_path: str) -> list[str]:
    domains: list[str] = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = row.get("domain", "").strip()
            if domain:
                domains.append(domain)
    return domains