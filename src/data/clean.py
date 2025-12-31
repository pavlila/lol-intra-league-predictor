from pathlib import Path

import numpy as np
import pandas as pd


class LoLDataCleaner:
    """
    A class to clean and aggregate League of Legends competitive match data
    from different sources GOL.gg and Oracle's Elixir.
    """

    def __init__(self):
        """
        Initializes the cleaner with file paths, team name mapping,
        and league/tournament configurations for 2023-2025.
        """
        BASE_DIR = Path(__file__).resolve().parents[2]
        self.base_input_path_golgg = f"{BASE_DIR}/scrap/golgg/data/"
        self.base_output_path_oracleselixir = f"{BASE_DIR}/scrap/oracleselixir/"

        self.replace_map = {
            "Edward Gaming": "EDward Gaming",
            "Hanwha Life eSports": "Hanwha Life Esports",
            "TALON": "PSG Talon",
            "BNK FearX": "BNK FEARX",
            "GIANTX": "GiantX",
            "OMG": "Oh My God",
            "Fluxo": "Fluxo W7M",
            "Gen.G eSports": "Gen.G",
            "Anyone s Legend": "Anyone's Legend",
            "Isurus Estral": "Isurus",
            "Funplus Phoenix": "FunPlus Phoenix",
            "OK BRION": "OKSavingsBank BRION",
            "TT": "ThunderTalk Gaming",
        }

        self.expected_cols = [
            "league",
            "date",
            "Team",
            "GP",
            "W",
            "L",
            "AGT",
            "K",
            "D",
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

        self.league_keywords = {
            "2023": ["LPL", "LEC", "LCK", "LCS", "CBLOL", "LLA", "PCS", "VCS", "LJL"],
            "2024": ["LPL", "LEC", "LCK", "LCS", "CBLOL", "LLA", "PCS", "VCS", "LJL"],
            "2025": ["LPL", "LEC", "LCK", "LTA N", "LTA S", "LCP"],
        }

        self.tournaments = {
            "2023": [
                "LPL Spring 2023",
                "LPL Spring Playoffs 2023",
                "LPL Summer 2023",
                "LPL Summer Playoffs 2023",
                "LPL Regional Finals 2023",
                "LEC Winter Groups 2023",
                "LEC Winter Playoffs 2023",
                "LEC Spring Season 2023",
                "LEC Spring Groups 2023",
                "LEC Spring Playoffs 2023",
                "LEC Summer 2023",
                "LEC Summer Groups 2023",
                "LEC Summer Playoffs 2023",
                "LEC Season Finals 2023",
                "LCK Spring 2023",
                "LCK Spring Playoffs 2023",
                "LCK Summer 2023",
                "LCK Summer Playoffs 2023",
                "LCK Regional Finals 2023",
                "LCS Spring 2023",
                "LCS Spring Playoffs 2023",
                "LCS Summer 2023",
                "LCS Championship 2023",
                "CBLOL Split 1 2023",
                "CBLOL Split 1 Playoffs 2023",
                "CBLOL Split 2 2023",
                "CBLOL Split 2 Playoffs 2023",
                "LLA Opening 2023",
                "LLA Opening Playoffs 2023",
                "LLA Closing 2023",
                "LLA Closing Playoffs 2023",
                "PCS Spring 2023",
                "PCS Spring Playoffs 2023",
                "PCS Summer 2023",
                "PCS Summer Playoffs 2023",
                "VCS Spring 2023",
                "VCS Spring Playoffs 2023",
                "VCS Summer 2023",
                "VCS Summer Playoffs 2023",
                "LJL Spring 2023",
                "LJL Spring Playoffs 2023",
                "LJL Summer 2023",
                "LJL Summer Playoffs 2023",
            ],
            "2024": [
                "LPL Spring 2024",
                "LPL Spring Playoffs 2024",
                "LPL Summer Placements 2024",
                "LPL Summer Season 2024",
                "LPL Summer Playoffs 2024",
                "LPL Regional Finals 2024",
                "LEC Winter Season 2024",
                "LEC Winter Playoffs 2024",
                "LEC Spring Season 2024",
                "LEC Spring Playoffs 2024",
                "LEC Summer Season 2024",
                "LEC Summer Playoffs 2024",
                "LEC Season Finals 2024",
                "LCK Spring 2024",
                "LCK Spring Playoffs 2024",
                "LCK Summer 2024",
                "LCK Summer Playoffs 2024",
                "LCK Regional Finals 2024",
                "LCS Spring 2024",
                "LCS Spring Playoffs 2024",
                "LCS Summer 2024",
                "LCS Championship 2024",
                "CBLOL Split 1 2024",
                "CBLOL Split 1 Playoffs 2024",
                "CBLOL Split 2 2024",
                "CBLOL Split 2 Playoffs 2024",
                "LLA Opening 2024",
                "LLA Opening Playoffs 2024",
                "LLA Closing 2024",
                "LLA Closing Playoffs 2024",
                "PCS Spring 2024",
                "PCS Spring Playoffs 2024",
                "PCS Summer 2024",
                "PCS Summer Playoffs 2024",
                "VCS Spring 2024",
                "VCS Spring Playoffs 2024",
                "VCS Summer 2024",
                "VCS Summer Playoffs 2024",
                "LJL Spring 2024",
                "LJL Spring Playoffs 2024",
                "LJL Summer 2024",
                "LJL Summer Playoffs 2024",
            ],
            "2025": [
                "LPL 2025 Split 1",
                "LPL 2025 Split 1 Playoffs",
                "LPL 2025 Split 2 Placements",
                "LPL 2025 Split 2",
                "LPL 2025 Split 2 Playoffs",
                "LPL 2025 Split 3",
                "LPL 2025 Grand Finals",
                "LPL 2025 Regional Finals",
                "LEC Winter 2025",
                "LEC 2025 Winter Playoffs",
                "LEC 2025 Spring Season",
                "LEC 2025 Spring Playoffs",
                "LEC 2025 Summer Season",
                "LEC 2025 Summer Playoffs",
                "LCK Cup 2025",
                "LCK 2025 Rounds 1-2",
                "LCK 2025 Road to MSI",
                "LCK 2025 Rounds 3-5",
                "LCK 2025 Season Play-In",
                "LCK 2025 Season Playoffs",
                "LTA North 2025 Split 1",
                "LTA North 2025 Split 2",
                "LTA North 2025 Split 2 Playoffs",
                "LTA North 2025 Split 3",
                "LTA South 2025 Split 1",
                "LTA South 2025 Split 2",
                "LTA South 2025 Split 2 Playoffs",
                "LTA South 2025 Split 3",
                "LCP 2025 Season Kickoff",
                "LCP 2025 Season Kickoff Qualifying Series",
                "LCP 2025 Mid Season",
                "LCP 2025 Mid Season Qualifying Series",
                "LCP 2025 Season Finals",
                "LCP 2025 Season Finals Playoffs",
            ],
        }

    def rename_teams_in_matches(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes team names in the DataFrame using a predefined map.

        Args:
            df (pd.DataFrame): Raw DataFrame containing match data with inconsistent team names.

        Returns:
            pd.DataFrame: DataFrame with corrected and unified team names.
        """
        df[["teamA", "teamB"]] = df[["teamA", "teamB"]].replace(self.replace_map).copy()
        return df

    def clean_matches(self, year: str) -> pd.DataFrame:
        """
        Loads match CSV files for a specific year and prepares basic match information.

        Args:
            year (str): The season year (e.g., "2023", "2024", "2025").

        Returns:
            pd.DataFrame: A cleaned DataFrame containing match dates, leagues, and win results.
        """
        tournaments = self.tournaments.get(year, [])
        df = pd.DataFrame()

        for t in tournaments:
            path = f"{self.base_input_path_golgg}{t}_matches.csv"
            data = pd.read_csv(path, sep=",")

            found_league = next(
                (l for l in self.league_keywords[year] if l in t), "Unknown"
            )
            data["league"] = found_league

            df = pd.concat([df, data], ignore_index=True)

        df["scoreA"] = pd.to_numeric(df["scoreA"], errors="coerce")
        df["scoreB"] = pd.to_numeric(df["scoreB"], errors="coerce")

        df = df[df["scoreA"] != df["scoreB"]]
        df["teamA_win"] = (df["scoreA"] > df["scoreB"]).astype(int)
        df = df.drop(columns=["scoreA", "scoreB"])

        df = self.rename_teams_in_matches(df)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        return df

    def aggregate_until_date(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates cumulative performance statistics for a team up to a specific date.

        Args:
            df (pd.DataFrame): Data containing all matches played by a team so far.

        Returns:
            pd.Series: A collection of calculated metrics like win rate, KD ratio, and objective control.
        """
        out = {}
        out["GP"] = len(df)
        out["W"] = df["result"].sum()
        out["L"] = out["GP"] - out["W"]
        out["AGT"] = df["AGT"].mean()
        out["K"] = df["teamkills"].sum()
        out["D"] = df["teamdeaths"].sum()
        out["KD"] = out["K"] / out["D"] if out["D"] > 0 else np.nan
        out["CKPM"] = df["CKPM"].mean()
        out["GSPD"] = df["gspd"].mean()
        out["GD15"] = df["GD15"].mean()
        out["FB%"] = df["firstblood"].mean()
        out["FT%"] = df["firsttower"].mean()
        out["F3T%"] = df["firsttothreetowers"].mean()
        out["PPG"] = df["turretplates"].mean()

        def get_rate(my_col, opp_col):
            total = df[my_col].sum() + df[opp_col].sum()
            return df[my_col].sum() / total if total > 0 else np.nan

        out["HLD%"] = get_rate("heralds", "opp_heralds")
        out["GRB%"] = get_rate("void_grubs", "opp_void_grubs")
        out["BN%"] = get_rate("barons", "opp_barons")
        out["ELD%"] = get_rate("elders", "opp_elders")
        out["DRG%"] = get_rate("dragons", "opp_dragons")

        out["FD%"] = df["firstdragon"].mean()
        out["FBN%"] = df["firstbaron"].mean()
        out["LNE%"] = df["LNE%"].mean()
        out["JNG%"] = df["JNG%"].mean()
        out["WPM"] = df["wpm"].mean()
        out["CWPM"] = df["CWPM"].mean()
        out["WCPM"] = df["WCPM"].mean()

        out["winrate%"] = out["W"] / out["GP"] if out["GP"] > 0 else np.nan
        return pd.Series(out)

    def clean_teams(self) -> pd.DataFrame:
        """
        Main processing method for teams data that reads Oracle's Elixir data and computes daily team statistics.

        Returns:
            pd.DataFrame: A final, large table of team performance metrics organized by date and league.
        """
        teams_2023 = pd.read_csv(
            f"{self.base_output_path_oracleselixir}2023_LoL_esports_match_data_from_OraclesElixir.csv",
            sep=",",
            low_memory=False,
        )
        teams_2024 = pd.read_csv(
            f"{self.base_output_path_oracleselixir}2024_LoL_esports_match_data_from_OraclesElixir.csv",
            sep=",",
            low_memory=False,
        )
        teams_2025 = pd.read_csv(
            f"{self.base_output_path_oracleselixir}2025_LoL_esports_match_data_from_OraclesElixir.csv",
            sep=",",
            low_memory=False,
        )

        teams = [teams_2023, teams_2024, teams_2025]

        res = pd.DataFrame()

        for i in range(len(teams)):
            year = str(2023 + i)

            for l in self.league_keywords.get(year, []):
                data = (
                    teams_2023
                    if year == "2023"
                    else teams_2024 if year == "2024" else teams_2025
                )

                df = data[data["league"].str.upper() == f"{l.upper()}"].copy()

                df["date"] = pd.to_datetime(df["date"])
                df["AGT"] = df["gamelength"] / 60

                players = df[df["participantid"] < 100].copy()

                game_totals = (
                    players.groupby("gameid")
                    .agg(
                        total_minions=("minionkills", "sum"),
                        total_jungle=("monsterkills", "sum"),
                    )
                    .reset_index()
                )

                df = df.merge(game_totals, on="gameid", how="left")

                df["LNE%"] = df["minionkills"] / df["total_minions"]
                df["JNG%"] = df["monsterkills"] / df["total_jungle"]

                df = df[df["participantid"].isin([100, 200])].copy()
                df = df.sort_values("date")

                df["K+D"] = df["teamkills"] + df["teamdeaths"]
                df["CKPM"] = df["K+D"] / df["AGT"]
                df["GD15"] = df["goldat15"] - df["opp_goldat15"]

                df["CWPM"] = (
                    pd.to_numeric(df["controlwardsbought"], errors="coerce") / df["AGT"]
                )
                df["WCPM"] = (
                    pd.to_numeric(df["wardskilled"], errors="coerce") / df["AGT"]
                )

                daily_stats = []
                for (league, team, split, playoffs), group in df.groupby(
                    ["league", "teamname", "split", "playoffs"]
                ):
                    group = group.sort_values("date")
                    for day in group["date"].dt.date.unique():
                        subset = group[group["date"].dt.date <= day]
                        stats = self.aggregate_until_date(subset)
                        stats["league"] = league
                        stats["split"] = split
                        stats["playoffs"] = playoffs
                        stats["date"] = pd.Timestamp(day)
                        stats["Team"] = team
                        daily_stats.append(stats)

                df_final = pd.DataFrame(daily_stats)

                for c in self.expected_cols:
                    if c not in df_final.columns:
                        df_final[c] = np.nan

                df_final = df_final[self.expected_cols]
                res = pd.concat([res, df_final], ignore_index=True)

        return res
