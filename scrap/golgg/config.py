from pathlib import Path

BASE_URL = "https://gol.gg"
RAW_DIR = Path("../data/raw")
INTER_DIR = Path("../data/intermediate")

USER_AGENT = "golgg-scraper/0.1 (ladislav.pavlicek.2004@gmail.com)"
REQUEST_DELAY = 1.0
MAX_RETRIES = 5
TIMEOUT = 20