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

    if not table:
        return result
    
    for tr in table.find_all('tr')[1:]:
        tds = tr.find_all('td')
        if len(tds) < 5:
            continue

        game_cell = tds[0]
        teams = [a.get_text(strip=True) for a in game_cell.find_all('a')]
        team_left = teams[0] if len(teams) > 0 else ""
        team_right = teams[1] if len(teams) > 1 else ""

        winner = tds[1].get_text(strip=True)
        loser = team_right if winner == team_left else team_left

        score_text = tds[2].get_text(strip=True)
        scoreA, scoreB = parse_score(score_text)

        if scoreA is not None and scoreB is not None:
            if scoreA > scoreB:
                teamA, teamB = winner, loser
            else:
                teamA, teamB = loser, winner

        date_text = tds[5].get_text(strip=True) if len(tds) > 5 else ""
        date= try_parse_date(date_text)

        result.append({
            "teamA": teamA,
            "teamB": teamB,
            "scoreA": scoreA,
            "scoreB": scoreB,
            "date": date
        })

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


        