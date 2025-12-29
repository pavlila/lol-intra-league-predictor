from pathlib import Path

BASE_URL = "https://gol.gg"
PROJECT_DIR = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_DIR / "scrap/golgg/data"

USER_AGENT = "golgg-scraper/0.1 (ladislav.pavlicek.2004@gmail.com)"
REQUEST_DELAY = 1.0
MAX_RETRIES = 5
TIMEOUT = 20
