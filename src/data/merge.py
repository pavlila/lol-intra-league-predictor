import pandas as pd

def concatDfs(years):
    return pd.concat(years, ignore_index=True)

def getStats(team, league, date, teamsStats):
    # 1. Najdi veškerou historii týmu v této lize před daným datem
    teamDataPast = teamsStats[
        (teamsStats['Team'] == team) & 
        (teamsStats['league'] == league) & 
        (teamsStats['date'] < date)
    ].sort_values('date', ascending=False)

    if teamDataPast.empty:
        return pd.Series(dtype=float)

    # Nejčerstvější data, co máme (i kdyby GP bylo jen 1)
    teamLastData = teamDataPast.iloc[0]

    # Pokud už máme v aktuálním splitu/roce dost dat, použijeme je přímo
    if teamLastData.GP > 5:
        return teamLastData.drop(labels=['date','Team','league'], errors='ignore')

    # Pokud máme GP <= 5, hledáme v historii STEJNÉ ligy záznam, kde bylo GP > 5
    # (Tzn. hledáme konec předchozího splitu/sezóny této ligy)
    stable_past_data = teamDataPast[teamDataPast['GP'] > 5]

    if stable_past_data.empty:
        # Pokud jsme v této lize nikdy nenašli stabilní data (GP > 5), 
        # vrátíme prázdno (zápas se zahodí)
        return pd.Series(dtype=float)

    # Nejnovější stabilní záznam z minulosti
    teamLastStable = stable_past_data.iloc[0]

    # --- LOGIKA SPOJENÍ (Vážený průměr) ---
    gp_stable = min(teamLastStable.GP, 5) # Omezíme vliv starých dat, aby nová měla váhu
    gp_curr = teamLastData.GP
    gp_total = gp_stable + gp_curr

    combined_data = pd.Series(dtype=float)
    combined_data['GP'] = gp_total

    numeric_cols = [
        'AGT','KD','CKPM','GSPD','GD15',
        'FB%','FT%','F3T%','PPG','HLD%','GRB%','FD%','DRG%','ELD%',
        'FBN%','BN%','LNE%','JNG%','WPM','CWPM','WCPM','winrate%'
    ]

    # Spočítáme vážený průměr pro všechny metriky
    for col in numeric_cols:
        if col in teamLastData and col in teamLastStable:
            combined_data[col] = (
                (teamLastData[col] * gp_curr) + (teamLastStable[col] * gp_stable)
            ) / gp_total

    return combined_data

def mergeMatchesAndTeamsData(matches, teams):
    merged_rows = []
    for _, row in matches.iterrows():
        teamA = row['teamA']
        teamB = row['teamB']
        date = row['date']
        league = row['league']
        win = row['teamA_win']

        statsA = getStats(teamA, league, date, teams)
        statsB = getStats(teamB, league, date, teams)

        if statsA.empty or statsB.empty:
            continue

        statsA = statsA[[col for col in statsA.index if col not in ['Team','league','date','teamA_win']]]
        statsB = statsB[[col for col in statsB.index if col not in ['Team','league','date','teamA_win']]]

        statsA = statsA.add_suffix("_A")
        statsB = statsB.add_suffix("_B")

        combined_data = pd.concat([statsA, statsB])

        combined_data['teamA'] = teamA
        combined_data['teamB'] = teamB
        combined_data['date'] = date
        combined_data['league'] = league
        combined_data['teamA_win'] = win

        merged_rows.append(combined_data)

    return pd.DataFrame(merged_rows).reset_index(drop=True)

dfs_matches = ['2023','2024','2025']
matches_list = [pd.read_csv(f"../../data/cleaned/matches/{match}.csv", sep=',') for match in dfs_matches]
matches = concatDfs(matches_list)

dfs_teams = ['2023','2024','2025']
teams_list = [pd.read_csv(f"../../data/cleaned/teams/{team}.csv", sep=',') for team in dfs_teams]
teams = concatDfs(teams_list)

data = mergeMatchesAndTeamsData(matches, teams)

data.to_csv("../../data/merged/data.csv", sep=',', index=False)
