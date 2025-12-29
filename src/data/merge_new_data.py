import pandas as pd


class LoLNewDataMerger:
    """
    A class to merge upcoming match data with historical performance statistics.
    Designed specifically to prepare new data for real-time predictions.
    """

    def __init__(self):
        """
        Initializes the merger with a standard list of numeric performance metrics.
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
        Retrieves historical statistics for a team before a specific date.
        If current season data is insufficient, it blends it with the last
        stable performance data using a weighted average.

        Args:
            team (str): The name of the team.
            league (str): The league context.
            date (pd.Timestamp): The date of the upcoming match.
            teamsStats (pd.DataFrame): The database of historical team performances.

        Returns:
            pd.Series: Weighted team statistics or an empty Series if no data exists.
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

    def merge_new_teams_and_matches(self, matches, teams):
        """
        Combines a list of new matches with historical stats for both competing teams.

        Args:
            matches (pd.DataFrame): New matches (teamA, teamB, date, league).
            teams (pd.DataFrame): Historical performance database.

        Returns:
            pd.DataFrame: A dataset enriched with historical features for prediction.
        """
        merged_rows = []
        missing_A = 0
        missing_B = 0

        for _, row in matches.iterrows():
            teamA, teamB = row["teamA"], row["teamB"]
            date, league = row["date"], row["league"]

            statsA = self.getStats(teamA, league, date, teams)
            statsB = self.getStats(teamB, league, date, teams)

            if statsA.empty:
                missing_A += 1
            if statsB.empty:
                missing_B += 1

            if statsA.empty or statsB.empty:
                continue

            statsA = statsA[
                [c for c in statsA.index if c not in ["Team", "league", "date"]]
            ]
            statsB = statsB[
                [c for c in statsB.index if c not in ["Team", "league", "date"]]
            ]

            statsA = statsA.add_suffix("_A")
            statsB = statsB.add_suffix("_B")

            combined_data = pd.concat([statsA, statsB])
            combined_data["teamA"] = teamA
            combined_data["teamB"] = teamB
            combined_data["date"] = date
            combined_data["league"] = league

            merged_rows.append(combined_data)

        print(
            f"Merge complete. Missing stats: Team A: {missing_A}, Team B: {missing_B}"
        )

        return pd.DataFrame(merged_rows).reset_index(drop=True)
