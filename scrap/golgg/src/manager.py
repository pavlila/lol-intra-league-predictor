from urllib.parse import quote
from fetcher import Fetcher
from parser_matchlist import GolParser
from config import BASE_URL, DATA_DIR
import csv
from pathlib import Path


class GolManager:
    """
    Manages the scraping workflow for GOL.gg tournaments.
    """

    def __init__(self):
        self.fetcher = Fetcher()
        self.parser = GolParser()
        self.base_url = BASE_URL

    def _slug_to_url(self, slug: str) -> str:
        encoded = quote(slug, safe="")
        return f"{self.base_url}/tournament/tournament-matchlist/{encoded}/"

    def scrape_tournament_matchlist(self, tournament_name: str, out_csv: Path = None):
        url = self._slug_to_url(tournament_name)
        resp = self.fetcher.get(url)

        matches = self.parser.parse_tournament_matchlist(resp.text)

        if not matches:
            print(f"[!] No matches found for {tournament_name}")
            return []

        if out_csv is None:
            safe_name = tournament_name.replace("/", "_")
            out_csv = DATA_DIR / f"{safe_name}_matches.csv"

        out_csv.parent.mkdir(parents=True, exist_ok=True)

        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=matches[0].keys())
            writer.writeheader()
            writer.writerows(matches)

        print(f"[OK] Saved {len(matches)} matches to {out_csv}")
        return matches

    def scrape_many(self, tournaments: list):
        for name in tournaments:
            try:
                self.scrape_tournament_matchlist(name)
            except Exception as e:
                print(f"[ERROR] Failed to scrape {name}: {e}")
                continue

    @staticmethod
    def load_tournaments_from_file(path: str):
        tournaments = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    tournaments.append(line)
        return tournaments
