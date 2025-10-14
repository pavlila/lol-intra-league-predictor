from bs4 import BeautifulSoup
from dateutil import parser as dparser
import re

def parse_tournament_matchlist(html):
    soup = BeautifulSoup(html, "html.parser")
    result = []

    table = None
    for t in soup.find_all('table'):
        headers = [th.get_text(strip=True).lower() for th in t.find_all("th")]
        if any(h in('score', 'patch', 'date', 'game') for h in headers):
            table = t
            break

    if table is None:
        table = soup.find('table')
    if not table:
        return result
    
    for tr in table.find_all('tr')[1:]:
        tds = tr.find_all('td')
        if len(tds) < 5:
            continue

        teamA = tds[1].get_text(strip=True)
        teamB = tds[3].get_text(strip=True)

        score_text = tds[2].get_text(strip=True)
        scoreA, scoreB = parse_score(score_text)

        date_text = tds[-1].get_text(strip=True) if len(tds) > 5 else ""
        date= try_parse_date(date_text)

        result.append({
            "teamA": teamA,
            "teamB": teamB,
            "scoreA": scoreA,
            "scoreB": scoreB,
            "date": date
        })

    print(f"[DEBUG] Parsed {len(result)} matches")
    return result

def parse_score(s):
    m = re.search(r"(\d+)\s*[-:]\s*(\d+)", s or "")
    if not m: return None, None
    return int(m.group(1)), int(m.group(2))

def try_parse_date(s):
    if not s: return ""
    try:
        return dparser.parse(s, fuzzy=True).date().isoformat()
    except Exception:
        return s


        