from pathlib import Path

BASE_URL = "https://gol.gg"
RAW_DIR = Path("../data/raw")
INTER_DIR = Path("../data/intermediate")

USER_AGENT = "golgg-scraper/0.1 (ladislav.pavlicek.2004@gmail.com)"
REQUEST_DELAY = 1.0 # cekani mezi requestami (1 sec)
MAX_RETRIES = 5 # pocet pokusu po chybe serveru
TIMEOUT = 20 # max cekani na odpoved