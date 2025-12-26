from urllib.parse import quote
from fetcher import Fetcher
from parser_matchlist import parse_tournament_matchlist
from config import BASE_URL, RAW_DIR, INTER_DIR
import csv, os

def slug_to_url(slug: str) -> str:
    encoded = quote(slug, safe='')
    return f"{BASE_URL}/tournament/tournament-matchlist/{encoded}/"

def scrape_tournament_matchlist(tournament_name: str, out_csv: str = None):
    url = slug_to_url(tournament_name)
    fetcher = Fetcher()
    resp = fetcher.get(url)

    html = resp.text

    matches = parse_tournament_matchlist(html)

    out_csv = out_csv or (INTER_DIR / f"{tournament_name.replace('/','_')}_matches.csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=matches[0].keys())
        writer.writeheader()
        writer.writerows(matches)
    print(f"[OK] Saved {len(matches)} matches to {out_csv}")
    return matches

def scrape_many(tournaments):
    for i, name in enumerate(tournaments):
        try:
            matches = scrape_tournament_matchlist(name)
        except Exception as e:
            continue

def load_tournaments_from_file(path: str):
    tournaments = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            tournaments.append(line)
    return tournaments