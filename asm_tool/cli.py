# File: asm_tool/cli.py

import logging
import warnings
import click
import typer

# Silence that one-off Wappalyzer regex warning
warnings.filterwarnings("ignore", message="Caught 'unbalanced parenthesis")

from asm_tool.config import INPUT_CSV
from asm_tool.input_parser import load_domains
from asm_tool.recon.subdomains import enumerate_subdomains
from asm_tool.recon.live_check import filter_live
from asm_tool.recon.dns_whois import get_dns_records, get_whois_info
from asm_tool.recon.port_scan import scan_ports
from asm_tool.recon.fingerprint import detect_technologies
from asm_tool.recon.ssl_analysis import analyze_ssl
from asm_tool.recon.headers_audit import audit_headers
from asm_tool.recon.osint import check_breach
from asm_tool.risk.scorer import compute_risk_score, ai_summary
from asm_tool.output import write_json_report

# Configure basic console logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = typer.Typer()

@app.command()
def run(input_file: str = None):
    """
    Run ASM tool on a list of domains.
    """
    csv_path = input_file or INPUT_CSV
    domains = load_domains(csv_path)

    # Domain-level progress bar
    with click.progressbar(
        domains,
        label="Scanning domains",
        show_eta=True,
        item_show_func=lambda d: d
    ) as bar:
        for domain in bar:
            logger.info(f"→ Starting scan for {domain}")

            # 1. Subdomain enumeration
            logger.info(" · Enumerating subdomains…")
            subdomains = enumerate_subdomains(domain)
            logger.info(f"   → Found {len(subdomains)} subdomains")

            # 2. Live host detection
            logger.info(" · Checking live hosts…")
            live_subs = filter_live(subdomains)
            logger.info(f"   → {len(live_subs)} live hosts")

            # 3. DNS & WHOIS lookup
            logger.info(" · Fetching DNS & WHOIS…")
            dns = get_dns_records(domain)
            whois = get_whois_info(domain)

            # 4. Port scanning (fast)
            logger.info(" · Scanning ports (fast)…")
            ports = scan_ports(domain)
            logger.info(f"   → {len(ports)} open ports")

            # 5. Technology stack detection
            logger.info(" · Detecting technologies…")
            techs = detect_technologies(f"https://{domain}")

            # 6. SSL/TLS analysis
            logger.info(" · Analyzing SSL/TLS…")
            ssl = analyze_ssl(domain)

            # 7. HTTP header audit
            logger.info(" · Auditing HTTP headers…")
            headers = audit_headers(domain)

            # 8. OSINT breach check
            logger.info(" · Checking breach history…")
            breaches = check_breach(domain)

            # 9. Aggregate findings
            logger.info(" · Compiling findings…")
            findings = {
                "subdomains": subdomains,
                "live_subdomains": live_subs,
                "dns_records": dns,
                "whois": whois,
                "open_ports": ports,
                "technologies": techs,
                "ssl_analysis": ssl,
                "headers": headers,
                "breaches": breaches,
            }

            # 10. Risk scoring & AI summary
            logger.info(" · Computing risk score…")
            score = compute_risk_score(findings)
            logger.info(" · Generating AI summary…")
            ai = ai_summary(findings)

            # 11. Write JSON report
            report = {
                "domain": domain,
                "risk_score": score,
                **ai,
                **findings
            }
            write_json_report(domain, report)
            logger.info(f"✓ Finished scan for {domain}")

    logger.info("✅ All domains scanned and reports generated.")

if __name__ == "__main__":
    app()
