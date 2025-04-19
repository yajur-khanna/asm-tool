import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
INPUT_CSV = os.getenv("INPUT_CSV", "input.csv")
HAVEIBEENPWNED_API_KEY = os.getenv("HAVEIBEENPWNED_API_KEY", "")
