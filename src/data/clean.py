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
        path = f"../../scrap/golgg/data/intermediate/{t}_matches.csv"
        data = pd.read_csv(path, sep=',')
        data['tournament'] = t
        df = pd.concat([df, data], ignore_index=True)

    df['scoreA'] = pd.to_numeric(df['scoreA'], errors='coerce')
    df['scoreB'] = pd.to_numeric(df['scoreB'], errors='coerce')

    df = df[df['scoreA'] != df['scoreB']]
    df['teamA_win'] = (df['scoreA'] > df['scoreB']).astype(int)
    df = df.drop(columns=['scoreA','scoreB'])

    # df = renameTeamsInMatches(df)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def teamsClean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess raw team statistics.

    This function converts numeric columns, calculates winrate, 
    normalizes percentage columns, and ensures proper date formatting.

    Specifically:
        - Converts 'W' (wins) and 'GP' (games played) to numeric
        - Creates 'winrate%' column as W / GP
        - Drops unused columns: ['W', 'L', 'K', 'D']
        - Converts percentage columns (e.g. 'FB%', 'FT%', 'GRB%') 
          from string with '%' to float in range [0, 1]
        - Converts 'date' to datetime

    Args:
        df (pd.DataFrame): Raw DataFrame of team statistics.

    Returns:
        pd.DataFrame: Cleaned DataFrame with numeric, normalized 
            percentage values and standardized columns.
    """
    df['W'] = pd.to_numeric(df['W'], errors='coerce').fillna(0)
    df['GP'] = pd.to_numeric(df['GP'], errors='coerce').fillna(0)
    df['winrate%'] = df['W'] / df['GP']

    df = df.drop(columns=['W','L','K','D'])
    percent_cols = ['FB%','FT%','F3T%','HLD%','GRB%','FD%','DRG%','ELD%','FBN%','GSPD','BN%','LNE%','JNG%']

    for col in percent_cols:
        if col in df.columns:
            df[col] = (df[col].astype(str).str.replace('%', '', regex=False).replace('nan', np.nan).astype(float) / 100)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

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

if __name__ == "__main__":
    main()