import re

from bs4 import BeautifulSoup
from dateutil import parser as dparser


class GolParser:
    """
    Parses tournament match data from GOL.gg HTML content.
    """

    def parse_tournament_matchlist(self, html):
        """
        Main parsing method that extracts match details from HTML.
        """
        soup = BeautifulSoup(html, "html.parser")
        result = []

        table = None
        for t in soup.find_all("table"):
            headers = [th.get_text(strip=True).lower() for th in t.find_all("th")]
            if any(h in ("score", "patch", "date", "game") for h in headers):
                table = t
                break

        if not table:
            table = soup.find("table")
        if not table:
            return result

        for tr in table.find_all("tr")[1:]:
            tds = tr.find_all("td")
            if len(tds) < 5:
                continue

            teamA = tds[1].get_text(strip=True)
            teamB = tds[3].get_text(strip=True)

            score_text = tds[2].get_text(strip=True)
            scoreA, scoreB = self._parse_score(score_text)

            date_text = tds[-1].get_text(strip=True) if len(tds) > 5 else ""
            date = self._try_parse_date(date_text)

            result.append(
                {
                    "teamA": teamA,
                    "teamB": teamB,
                    "scoreA": scoreA,
                    "scoreB": scoreB,
                    "date": date,
                }
            )

        return result

    def _parse_score(self, s):
        """
        Internal helper to extract scores using regex.
        """
        m = re.search(r"(\d+)\s*[-:]\s*(\d+)", s or "")
        if not m:
            return None, None
        return int(m.group(1)), int(m.group(2))

    def _try_parse_date(self, s):
        """
        Internal helper to format dates consistently.
        """
        if not s:
            return ""
        try:
            return dparser.parse(s, fuzzy=True).date().isoformat()
        except Exception:
            return s
