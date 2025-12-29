import pandas as pd


class LoLDataMerger:
    """
    A class to merge team performance statistics with match results.
    It calculates weighted stats for teams based on their history
    to prepare data for featuring.
    """

    def __init__(self):
        """
        Initializes the merger with a list of numeric columns to be processed.
        """
        self.numeric_cols = [
            "GP",
            "W",
            "L",
            "K",
            "D",
            "AGT",
            "KD",
            "CKPM",
            "GSPD",
            "GD15",
            "FB%",
            "FT%",
            "F3T%",
            "PPG",
            "HLD%",
            "GRB%",
            "FD%",
            "DRG%",
            "ELD%",
            "FBN%",
            "BN%",
            "LNE%",
            "JNG%",
            "WPM",
            "CWPM",
            "WCPM",
            "winrate%",
        ]

    def getStats(self, team, league, date, teamsStats):
        """
        Retrieves the most recent statistics for a specific team before a given date.
        If the team has played fewer than 5 games in the current split, it combines
        current data with stable data from the past
        (Past data from teams with more than five games are down-weighted).

        Args:
            team (str): Name of the team.
            league (str): The league the team plays in.
            date (pd.Timestamp): The date of the match to look back from.
            teamsStats (pd.DataFrame): DataFrame containing historical team statistics.

        Returns:
            pd.Series: A series of averaged or recent performance metrics for the team.
                       Returns an empty Series if no data is found.
        """

        teamDataPast = teamsStats[
            (teamsStats["Team"] == team)
            & (teamsStats["league"] == league)
            & (teamsStats["date"] < date)
        ].sort_values("date", ascending=False)

        if teamDataPast.empty:
            return pd.Series(dtype=float)

        teamLastData = teamDataPast.iloc[0]

        if teamLastData.GP > 5:
            return teamLastData.drop(labels=["date", "Team", "league"], errors="ignore")

        stable_past_data = teamDataPast[teamDataPast["GP"] > 5]

        if stable_past_data.empty:
            return pd.Series(dtype=float)

        teamLastStable = stable_past_data.iloc[0]

        gp_stable = min(teamLastStable.GP, 5)
        gp_curr = teamLastData.GP
        gp_total = gp_stable + gp_curr

        combined_data = pd.Series(dtype=float)
        combined_data["GP"] = gp_total

        for col in self.numeric_cols:
            if col in teamLastData and col in teamLastStable:
                combined_data[col] = (
                    (teamLastData[col] * gp_curr) + (teamLastStable[col] * gp_stable)
                ) / gp_total

        return combined_data

    def merge_teams_and_matches(self, matches, teams):
        """
        Iterates through all matches and joins them with the statistics of both
        competing teams (Team A and Team B).

        Args:
            matches (pd.DataFrame): DataFrame containing match schedules and winners.
            teams (pd.DataFrame): DataFrame containing daily team performance stats.

        Returns:
            pd.DataFrame: A unified DataFrame where each row represents a match
                         enriched with historical stats for both teams.
        """

        merged_rows = []
        missing_A = 0
        missing_B = 0
        for _, row in matches.iterrows():
            teamA = row["teamA"]
            teamB = row["teamB"]
            date = row["date"]
            league = row["league"]
            win = row["teamA_win"]

            statsA = self.getStats(teamA, league, date, teams)
            statsB = self.getStats(teamB, league, date, teams)

            if statsA.empty:
                missing_A += 1
            if statsB.empty:
                missing_B += 1
            if statsA.empty or statsB.empty:
                continue

            statsA = statsA[
                [
                    col
                    for col in statsA.index
                    if col not in ["Team", "league", "date", "teamA_win"]
                ]
            ]
            statsB = statsB[
                [
                    col
                    for col in statsB.index
                    if col not in ["Team", "league", "date", "teamA_win"]
                ]
            ]

            statsA = statsA.add_suffix("_A")
            statsB = statsB.add_suffix("_B")

            combined_data = pd.concat([statsA, statsB])

            combined_data["teamA"] = teamA
            combined_data["teamB"] = teamB
            combined_data["date"] = date
            combined_data["league"] = league
            combined_data["teamA_win"] = win

            merged_rows.append(combined_data)

        return pd.DataFrame(merged_rows).reset_index(drop=True)
