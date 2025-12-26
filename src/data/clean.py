import pandas as pd
import numpy as np

def renameTeamsInMatches(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize team names in a match dataset for consistency.

    This function replaces alternative spellings or legacy names 
    of teams in the 'teamA' and 'teamB' columns with a unified 
    naming convention. Useful for linking match data with other 
    datasets (e.g. team statistics).

    Args:
        df (pd.DataFrame): DataFrame of matches containing columns 
            'teamA' and 'teamB' with potentially inconsistent team names.

    Returns:
        pd.DataFrame: DataFrame with standardized team names in 
            columns 'teamA' and 'teamB'.
    """
    replace_map = {
        'Edward Gaming': 'EDward Gaming',
        'Hanwha Life eSports': 'Hanwha Life Esports',
        'TALON': 'PSG Talon',
        'BNK FearX': 'BNK FEARX',
        'GIANTX': 'GiantX',
        'OMG': 'Oh My God',
        'Fluxo': 'Fluxo W7M',
        'Gen.G eSports': 'Gen.G',
        'Anyone s Legend': "Anyone's Legend",
        'Isurus Estral': 'Isurus',
        'Funplus Phoenix': 'FunPlus Phoenix',
        'OK BRION': 'OKSavingsBank BRION',
        'TT': 'ThunderTalk Gaming'  
    }

    df[['teamA', 'teamB']] = df[['teamA', 'teamB']].replace(replace_map).copy()
    return df

def matchesClean(tournaments: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess raw match data.

    This function selects relevant columns from the raw matches dataset,
    standardizes team names, converts scores to numeric values, creates
    a binary target feature 'teamA_win', and parses the match date.

    Specifically:
        - Keeps only ['tournament', 'date', 'teamA', 'teamB', 'scoreA', 'scoreB']
        - Converts 'scoreA' and 'scoreB' to numeric
        - Creates new column 'teamA_win' (1 if teamA wins, else 0)
        - Drops 'scoreA' and 'scoreB'
        - Standardizes team names via 'renameTeamsInMatches'
        - Converts 'date' to datetime

    Args:
        df (pd.DataFrame): Raw matches DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame with columns:
            - 'tournament' (str)
            - 'date' (datetime64)
            - 'teamA' (str, standardized)
            - 'teamB' (str, standardized)
            - 'teamA_win' (int, 0/1)
    """

    df = pd.DataFrame()
    for t in tournaments:
        path = f"../../scrap/golgg/data/{t}_matches.csv"
        data = pd.read_csv(path, sep=',')
        
        league_keywords = ['LTA North', 'LTA South', 'LTA N', 'LTA S', 'LPL', 'LEC', 'LCK', 'LCS', 'CBLOL', 'LLA', 'PCS', 'VCS', 'LJL', 'LCP']

        found_league = next((l for l in league_keywords if l in t), "Unknown")
        data['league'] = found_league

        df = pd.concat([df, data], ignore_index=True)

    df['scoreA'] = pd.to_numeric(df['scoreA'], errors='coerce')
    df['scoreB'] = pd.to_numeric(df['scoreB'], errors='coerce')

    df = df[df['scoreA'] != df['scoreB']]
    df['teamA_win'] = (df['scoreA'] > df['scoreB']).astype(int)
    df = df.drop(columns=['scoreA','scoreB'])

    df = renameTeamsInMatches(df)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def teamsClean(data: pd.DataFrame, league: str) -> pd.DataFrame:
    l = data[data['league'].str.upper() == f'{league.upper()}'].copy()

    l['date'] = pd.to_datetime(l['date'])
    l['AGT'] = l['gamelength'] / 60

    players = l[l['participantid'] < 100].copy()
    
    game_totals = players.groupby('gameid').agg(
        total_minions=('minionkills', 'sum'),
        total_jungle=('monsterkills', 'sum')
    ).reset_index()

    l = l.merge(game_totals, on='gameid', how='left')

    l['LNE%'] = l['minionkills'] / l['total_minions']
    l['JNG%'] = l['monsterkills'] / l['total_jungle']

    l = l[l['participantid'].isin([100,200])].copy()
    l = l.sort_values('date')

    l['K+D'] = l['teamkills'] + l['teamdeaths']
    l['CKPM'] = l['K+D'] / l['AGT']
    l['GD15'] = l['goldat15'] - l['opp_goldat15']

    l['CWPM'] = pd.to_numeric(l['controlwardsbought'], errors='coerce') / l['AGT']
    l['WCPM'] = pd.to_numeric(l['wardskilled'], errors='coerce') / l['AGT']

    def aggregate_until_date(df: pd.DataFrame) -> pd.DataFrame:
        out = {}
        out['GP'] = len(df)
        out['W'] = df['result'].sum()
        out['L'] = out['GP'] - out['W']
        out['AGT'] = df['AGT'].mean()
        out['K'] = df['teamkills'].sum()
        out['D'] = df['teamdeaths'].sum()
        out['KD'] = out['K'] / out['D'] if out['D'] > 0 else np.nan
        out['CKPM'] = df['CKPM'].mean()
        out['GSPD'] = df['gspd'].mean()
        out['GD15'] = df['GD15'].mean()
        out['FB%'] = df['firstblood'].mean()
        out['FT%'] = df['firsttower'].mean()
        out['F3T%'] = df['firsttothreetowers'].mean()
        out['PPG'] = df['turretplates'].mean()

        def get_rate(my_col, opp_col):
            total = df[my_col].sum() + df[opp_col].sum()
            return df[my_col].sum() / total if total > 0 else np.nan

        out['HLD%'] = get_rate('heralds', 'opp_heralds')
        out['GRB%'] = get_rate('void_grubs', 'opp_void_grubs')
        out['BN%'] = get_rate('barons', 'opp_barons')
        out['ELD%'] = get_rate('elders', 'opp_elders')
        out['DRG%'] = get_rate('dragons', 'opp_dragons')

        out['FD%'] = df['firstdragon'].mean()
        out['FBN%'] = df['firstbaron'].mean()
        out['LNE%'] = df['LNE%'].mean()
        out['JNG%'] = df['JNG%'].mean()
        out['WPM'] = df['wpm'].mean()
        out['CWPM'] = df['CWPM'].mean()
        out['WCPM'] = df['WCPM'].mean()

        out['winrate%'] = out['W'] / out['GP'] if out['GP'] > 0 else np.nan
        return pd.Series(out)
    
    daily_stats = []
    for (league, team, split, playoffs), group in l.groupby(['league','teamname','split','playoffs']):
        group = group.sort_values('date')
        for day in group['date'].dt.date.unique():
            subset = group[group['date'].dt.date <= day]
            stats = aggregate_until_date(subset)
            stats['league'] = league
            stats['split'] = split
            stats['playoffs'] = playoffs
            stats['date'] = pd.Timestamp(day)
            stats['Team'] = team
            daily_stats.append(stats)

    l_final = pd.DataFrame(daily_stats)

    expected_cols = [
        "league", "date", "Team",
        "GP", "W", "L", "AGT", "K", "D", "KD", "CKPM",
        "GSPD", "GD15", "FB%", "FT%", "F3T%", "PPG",
        "HLD%", "GRB%", "FD%", "DRG%", "ELD%", "FBN%", "BN%",
        "LNE%", "JNG%", "WPM", "CWPM", "WCPM", "winrate%"
    ]

    for c in expected_cols:
        if c not in l_final.columns:
            l_final[c] = np.nan

    # teď vyber všechny očekávané sloupce
    l_final = l_final[expected_cols].sort_values(
        by=["league", "Team", "date"]
    ).reset_index(drop=True)
        
    return l_final


def main() -> None:
    """
    Batch process for cleaning match and team data.

    Reads raw CSV files, applies cleaning functions, 
    and saves cleaned datasets.
    """
 
    tournaments_2023 = [
        'LPL Spring 2023',
        'LPL Spring Playoffs 2023',
        'LPL Summer 2023',
        'LPL Summer Playoffs 2023',
        'LPL Regional Finals 2023',
        'LEC Winter Groups 2023',
        'LEC Winter Playoffs 2023',
        'LEC Spring Season 2023',
        'LEC Spring Groups 2023',
        'LEC Spring Playoffs 2023',
        'LEC Summer 2023',
        'LEC Summer Groups 2023',
        'LEC Summer Playoffs 2023',
        'LEC Season Finals 2023',
        'LCK Spring 2023',
        'LCK Spring Playoffs 2023',
        'LCK Summer 2023',
        'LCK Summer Playoffs 2023',
        'LCK Regional Finals 2023',
        'LCS Spring 2023',
        'LCS Spring Playoffs 2023',
        'LCS Summer 2023',
        'LCS Championship 2023',
        'CBLOL Split 1 2023',
        'CBLOL Split 1 Playoffs 2023',
        'CBLOL Split 2 2023',
        'CBLOL Split 2 Playoffs 2023',
        'LLA Opening 2023',
        'LLA Opening Playoffs 2023',
        'LLA Closing 2023',
        'LLA Closing Playoffs 2023',
        'PCS Spring 2023',
        'PCS Spring Playoffs 2023',
        'PCS Summer 2023',
        'PCS Summer Playoffs 2023',
        'VCS Spring 2023',
        'VCS Spring Playoffs 2023',
        'VCS Summer 2023',
        'VCS Summer Playoffs 2023',
        'LJL Spring 2023',
        'LJL Spring Playoffs 2023',
        'LJL Summer 2023',
        'LJL Summer Playoffs 2023',
    ] 

    tournaments_2024 = [
        'LPL Spring 2024',
        'LPL Spring Playoffs 2024',
        'LPL Summer Placements 2024',
        'LPL Summer Season 2024',
        'LPL Summer Playoffs 2024',
        'LPL Regional Finals 2024',
        'LEC Winter Season 2024',
        'LEC Winter Playoffs 2024',
        'LEC Spring Season 2024',
        'LEC Spring Playoffs 2024',
        'LEC Summer Season 2024',
        'LEC Summer Playoffs 2024',
        'LEC Season Finals 2024',
        'LCK Spring 2024',
        'LCK Spring Playoffs 2024',
        'LCK Summer 2024',
        'LCK Summer Playoffs 2024',
        'LCK Regional Finals 2024',
        'LCS Spring 2024',
        'LCS Spring Playoffs 2024',
        'LCS Summer 2024',
        'LCS Championship 2024',
        'CBLOL Split 1 2024',
        'CBLOL Split 1 Playoffs 2024',
        'CBLOL Split 2 2024',
        'CBLOL Split 2 Playoffs 2024',
        'LLA Opening 2024',
        'LLA Opening Playoffs 2024',
        'LLA Closing 2024',
        'LLA Closing Playoffs 2024',
        'PCS Spring 2024',
        'PCS Spring Playoffs 2024',
        'PCS Summer 2024',
        'PCS Summer Playoffs 2024',
        'VCS Spring 2024',
        'VCS Spring Playoffs 2024',
        'VCS Summer 2024',
        'VCS Summer Playoffs 2024',
        'LJL Spring 2024',
        'LJL Spring Playoffs 2024',
        'LJL Summer 2024',
        'LJL Summer Playoffs 2024'
    ]

    tournaments_2025 = [
        'LPL 2025 Split 1',
        'LPL 2025 Split 1 Playoffs',
        'LPL 2025 Split 2 Placements',
        'LPL 2025 Split 2',
        'LPL 2025 Split 2 Playoffs',
        'LPL 2025 Split 3',
        'LPL 2025 Grand Finals',
        'LPL 2025 Regional Finals',
        'LEC Winter 2025',
        'LEC 2025 Winter Playoffs',
        'LEC 2025 Spring Season',
        'LEC 2025 Spring Playoffs',
        'LEC 2025 Summer Season',
        'LEC 2025 Summer Playoffs',
        'LCK Cup 2025',
        'LCK 2025 Rounds 1-2',
        'LCK 2025 Road to MSI',
        'LCK 2025 Rounds 3-5',
        'LCK 2025 Season Play-In',
        'LCK 2025 Season Playoffs',
        'LTA North 2025 Split 1',
        'LTA North 2025 Split 2',
        'LTA North 2025 Split 2 Playoffs',
        'LTA North 2025 Split 3',
        'LTA South 2025 Split 1',
        'LTA South 2025 Split 2',
        'LTA South 2025 Split 2 Playoffs',
        'LTA South 2025 Split 3',
        'LCP 2025 Season Kickoff',
        'LCP 2025 Season Kickoff Qualifying Series',
        'LCP 2025 Mid Season',
        'LCP 2025 Mid Season Qualifying Series',
        'LCP 2025 Season Finals',
        'LCP 2025 Season Finals Playoffs'
    ]


    matches_2023 = matchesClean(tournaments_2023)
    matches_2024 = matchesClean(tournaments_2024)
    matches_2025 = matchesClean(tournaments_2025)

    matches_2023.to_csv(f"../../data/cleaned/matches/2023.csv", sep=',', index=False)
    matches_2024.to_csv(f"../../data/cleaned/matches/2024.csv", sep=',', index=False)
    matches_2025.to_csv(f"../../data/cleaned/matches/2025.csv", sep=',', index=False)

    teams_2023 = pd.read_csv("../../scrap/oracleselixir/2023_LoL_esports_match_data_from_OraclesElixir.csv", sep=',', low_memory=False)
    teams_2024 = pd.read_csv("../../scrap/oracleselixir/2024_LoL_esports_match_data_from_OraclesElixir.csv", sep=',', low_memory=False)
    teams_2025 = pd.read_csv("../../scrap/oracleselixir/2025_LoL_esports_match_data_from_OraclesElixir.csv", sep=',', low_memory=False)

    lec_2023 = teamsClean(teams_2023, 'LEC')
    lec_2024 = teamsClean(teams_2024, 'LEC')
    lec_2025 = teamsClean(teams_2025, 'LEC')

    lpl_2023 = teamsClean(teams_2023, 'LPL')
    lpl_2024 = teamsClean(teams_2024, 'LPL')
    lpl_2025 = teamsClean(teams_2025, 'LPL')

    lck_2023 = teamsClean(teams_2023, 'LCK')
    lck_2024 = teamsClean(teams_2024, 'LCK')
    lck_2025 = teamsClean(teams_2025, 'LCK')

    lta_south_2025 = teamsClean(teams_2025, 'LTA S')
    lta_north_2025 = teamsClean(teams_2025, 'LTA N')
    lcs_2024 = teamsClean(teams_2024, 'LCS')
    lcs_2023 = teamsClean(teams_2023, 'LCS')
    cblol_2024 = teamsClean(teams_2024, 'CBLOL')
    cblol_2023 = teamsClean(teams_2023, 'CBLOL')
    lla_2024 = teamsClean(teams_2024, 'LLA')
    lla_2023 = teamsClean(teams_2023, 'LLA')

    lcp_2025 = teamsClean(teams_2025, 'LCP')
    pcs_2024 = teamsClean(teams_2024, 'PCS')
    pcs_2023 = teamsClean(teams_2023, 'PCS')
    vcs_2024 = teamsClean(teams_2024, 'VCS')
    vcs_2023 = teamsClean(teams_2023, 'VCS')
    ljl_2024 = teamsClean(teams_2024, 'LJL')
    ljl_2023 = teamsClean(teams_2023, 'LJL')

    teams_2023 = pd.concat([lec_2023, lpl_2023, lck_2023, lcs_2023, cblol_2023, lla_2023, pcs_2023, vcs_2023, ljl_2023], ignore_index=True)
    teams_2024 = pd.concat([lec_2024, lpl_2024, lck_2024, lcs_2024, cblol_2024, lla_2024, pcs_2024, vcs_2024, ljl_2024], ignore_index=True)
    teams_2025 = pd.concat([lec_2025, lpl_2025, lck_2025, lta_south_2025, lta_north_2025, lcp_2025], ignore_index=True)

    teams_2023.to_csv(f"../../data/cleaned/teams/2023.csv", sep=',', index=False)
    teams_2024.to_csv(f"../../data/cleaned/teams/2024.csv", sep=',', index=False)
    teams_2025.to_csv(f"../../data/cleaned/teams/2025.csv", sep=',', index=False)

if __name__ == "__main__":
    main()