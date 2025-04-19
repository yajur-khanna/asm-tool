import os
import openai
from asm_tool.config import OPENAI_API_KEY

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY


def compute_risk_score(findings: dict) -> int:
    """
    Compute a heuristic risk score (0-100) based on findings.
    Weights (example):
      - 20%: number of live subdomains
      - 30%: number of open ports
      - 25%: number of tech fingerprints
      - 25%: number of breaches
    """
    live_subs = len(findings.get("live_subdomains", []))
    open_ports = len(findings.get("open_ports", []))
    techs = len(findings.get("technologies", []))
    breaches = len(findings.get("breaches", []))

    # Raw weighted score
    score = (
        0.2 * min(live_subs, 50) +
        0.3 * min(open_ports, 100) +
        0.25 * min(techs, 20) +
        0.25 * min(breaches, 10)
    )
    # Normalize to 0-100 scale
    max_raw = 0.2*50 + 0.3*100 + 0.25*20 + 0.25*10
    normalized = (score / max_raw) * 100
    return int(min(max(normalized, 0), 100))


def ai_summary(findings: dict) -> dict:
    """
    Use an LLM to generate a risk summary and remediation suggestions.
    """
    prompt = (
        "You are a security analyst. Given the following findings from an attack surface scan, "
        "provide a concise risk summary (1-2 sentences) and three prioritized remediation steps.\n\n"
        f"Findings: {findings}\n\nSummary and Recommendations:"
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        text = resp.choices[0].message.content.strip()
        # Split summary and recommendations by delimiter if provided
        parts = text.split("Recommendations:")
        summary = parts[0].strip()
        recs = []
        if len(parts) > 1:
            recs = [line.strip('- ').strip() for line in parts[1].splitlines() if line.strip()]
        return {"risk_summary": summary, "recommendations": recs}
    except Exception as e:
        # Fallback if API fails
        return {"risk_summary": "", "recommendations": []}


# File: asm_tool/output.py
import os
import json
from datetime import datetime
from asm_tool.utils import init_logger

logger = init_logger()


def write_json_report(domain: str, report: dict, out_dir: str = "reports") -> None:
    """
    Write the scan report as JSON to reports/{domain}.json
    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{domain.replace('.', '_')}_{timestamp}.json"
    path = os.path.join(out_dir, filename)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Wrote report for {domain} to {path}")
    except Exception as e:
        logger.error(f"Failed to write report for {domain}: {e}")


# File: asm_tool/utils.py
import logging
import subprocess


def init_logger(level: str = "INFO") -> logging.Logger:
    """
    Initialize and return a logger for the ASM tool.
    """
    logger = logging.getLogger("asm_tool")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger


def run_subprocess(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """
    Wrap subprocess.run to execute external commands and log errors.
    """
    logger = logging.getLogger("asm_tool.subprocess")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, **kwargs)
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command {cmd} failed: {e.stderr}")
        raise
