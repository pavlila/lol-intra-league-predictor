# lol-intra-league-predictor

This project predicts the outcomes of League of Legends matches within individual leagues using match data from [gol.gg](https://gol.gg/) and team statistics from [oracleselixir.com](https://oracleselixir.com/). 
It focuses exclusively on intra-league predictions. 
The model dynamically adapts to the most up-to-date team statistics and performance within each tournament.

## Used tournaments

<details>
<summary><b>Click to expand 2025 Tournaments</b></summary>
        
- LPL

        LPL 2025 Split 1 

        LPL 2025 Split 1 Playoffs

        LPL 2025 Split 2 Placements

        LPL 2025 Split 2

        LPL 2025 Split 2 Playoffs

        LPL 2025 Split 3

        LPL 2025 Grand Finals

        LPL 2025 Regional Finals

- LEC

        LEC 2025 Winter

        LEC 2025 Winter Playoffs

        LEC 2025 Spring Season

        LEC 2025 Spring Playoffs

        LEC 2025 Summer Season

        LEC 2025 Summer Playoffs

- LCK

        LCK 2025 Cup

        LCK 2025 Rounds 1-2

        LCK 2025 Road to MSI

        LCK 2025 Rounds 3-5

- LTA N

        LTA North 2025 Split 1

        LTA North 2025 Split 2

        LTA North 2025 Split 2 Playoffs

        LTA North 2025 Split 3

- LTA S

        LTA South 2025 Split 1

        LTA South 2025 Split 2

        LTA South 2025 Split 2 Playoffs

        LTA South 2025 Split 3

- LCP

        LCP 2025 Season Kickoff

        LCP 2025 Season Kickoff Qualifying Series

        LCP 2025 Mid Season

        LCP 2025 Mid Season Qualifying Series

        LCP 2025 Season Finals

        LCP 2025 Season Finals Playoffs
</details>

<details>
<summary><b>Click to expand 2024 Tournaments</b></summary>
        
- LPL

        LPL Spring 2024
  
        LPL Spring Playoffs 2024
  
        LPL Summer Placements 2024
  
        LPL Summer Season 2024
  
        LPL Summer Playoffs 2024
  
        LPL Regional Finals 2024

- LEC

        LEC Winter Season 2024

        LEC Winter Playoffs 2024

        LEC Spring Season 2024

        LEC Spring Playoffs 2024

        LEC Summer Season 2024

        LEC Summer Playoffs 2024

        LEC Season Finals 2024

- LCK

        LCK Spring 2024

        LCK Spring Playoffs 2024

        LCK Summer 2024

        LCK Summer Playoffs 2024

        LCK Regional Finals 2024

- LCS

        LCS Spring 2024

        LCS Spring Playoffs 2024

        LCS Summer 2024

        LCS Championship 2024

- CBLOL

        CBLOL Split 1 2024

        CBLOL Split 1 Playoffs 2024

        CBLOL Split 2 2024

        CBLOL Split 2 Playoffs 2024

- LLA

        LLA Opening 2024

        LLA Opening Playoffs 2024

        LLA Closing 2024 

        LLA Closing Playoffs 2024

- PCS

        PCS Spring 2024

        PCS Spring Playoffs 2024

        PCS Summer 2024

        PCS Summer Playoffs 2024

- VCS

        VCS Spring 2024

        VCS Spring Playoffs 2024

        VCS Summer 2024

        VCS Summer Playoffs 2024

- LJL

        LJL Spring 2024

        LJL Spring Playoffs 2024

        LJL Summer 2024

        LJL Summer Playoffs 2024
</details>

<details>
<summary><b>Click to expand 2023 Tournaments</b></summary>
        
- LPL

        LPL Spring 2023

        LPL Spring Playoffs 2023
  
        LPL Summer 2023

        LPL Summer Playoffs 2023

        LPL Regional Finals 2023

- LEC

        LEC Winter 2023

        LEC Winter Groups 2023

        LEC Winter Playoffs 2023

        LEC Spring Season 2023

        LEC Spring Groups 2023

        LEC Spring Playoffs 2023

        LEC Summer 2023

        LEC Summer Groups 2023

        LEC Summer Playoffs 2023

        LEC Season Finals 2023

- LCK

        LCK Spring 2023

        LCK Spring Playoffs 2023

        LCK Summer 2023

        LCK Summer Playoffs 2023

        LCK Regional Finals 2023

- LCS

        LCS Spring 2023

        LCS Spring Playoffs 2023

        LCS Summer 2023

        LCS Championship 2023

- CBLOL

        CBLOL Split 1 2023

        CBLOL Split 1 Playoffs 2023

        CBLOL Split 2 2023

        CBLOL Split 2 Playoffs 2023

- LLA

        LLA Opening 2023

        LLA Opening Playoffs 2023

        LLA Closing 2023

        LLA Closing Playoffs 2023

- PCS

        PCS Spring 2023

        PCS Spring Playoffs 2023

        PCS Summer 2023

        PCS Summer Playoffs 2023

- VCS

        VCS Spring 2023

        VCS Spring Playoffs 2023

        VCS Summer 2023

        VCS Summer Playoffs 2023

- LJL

        LJL Spring 2023

        LJL Spring Playoffs 2023

        LJL Summer 2023

        LJL Summer Playoffs 2023
</details>


## Scraping data

- [oracleselixir.com](https://oracleselixir.com/):
  
  The website provides a yearly CSV file containing all available data.  
  This file is downloaded directly into the `scrap/oracleselixir` directory.

- [gol.gg](https://gol.gg/):
  
  A custom scraper is used to collect match data from this source.

  - `scrap/golgg/src/tournaments.txt` contains the list of tournaments to be scraped  
  - `scrap/golgg/src/scraped_tournaments.txt` keeps track of tournaments that have already been scraped
 
  
  To run the scraper:

  ```bash
  uv run python scrap/golgg/src/main.py

## Data Preprocessing

- [gol.gg](https://gol.gg/):
  
  The match data is processed in a forward-only manner to prevent data leakage.  
  The match outcome is converted into a binary target variable.

- [oracleselixir.com](https://oracleselixir.com/)
  
  Since the full dataset is downloaded from the website, extensive preprocessing is required.  
  The list of engineered features is described in the **About Data** section.

  Data consistency checks are implemented to verify that the processed data matches the values presented on the website.

  To run the preprocessing tests:

  ```bash
  uv run pytest

## About data

<details>
<summary><b>Click to expand Data details</b></summary>

  - All the data presented below comes after the data cleaning phase

     - Matches data
   
           teamA: Name of the First Team
       
           teamB: Name of the Second Team

           date: Date of the Match
       
           league: League Name

           teamA_win: Binary outcome - 1 if the first team wins, 0 if the second team wins

     - Teams data
   
           league: League Name

           date: Date on which the statistic was recorded (aggregated from the start of the tournament up to this date

           Team: Team Name

           GP: Games Played
   
           W: Number of wins
   
           L: Number of losses

           AGT: Average game time/duration, in minutes
   
           K: Overall Kills
   
           D: Overall Deaths

           KD: Kill-to-Death Ratio

           CKPM: Average combined kills per minute (team kills + opponent kills)

           GSPD: Average gold spent percentage difference

           GD15: Average gold difference at 15 minutes

           FB%: First Blood rate -- for players/champions, percent of games earning a First Blood participation (kill or assist)

           FT%: First tower rate

           F3T%: First-to-three-towers rate (percentage of games in which team was the first to 3 tower kills)

           PPG: Turret plates destroed per game

           HLD%: Rift Herald control rate

           GRB%: Void Grub control rate

           FD%: First dragon rate

           DRG%: Dragon control rate: percent of all Dragons killed that were taken by the team, reflecting only elemental drakes if ELD% is present

           ELD%: Elder dragon control rate

           FBN%: First Baron rate

           BN%: Baron control rate

           LNE%: Lane Control: average share of game's total lane CS

           JNG%: Jungle Control: average share of game's total jungle CS

           WPM: Average wards placed per minute

           CWPM: Control wards puschased per minute

           WCPM: Average wards cleared per minute

           winrate%: W/GP ratio (Win/Games Played)
</details>

## Team-Match Linking Logic

    *update - threshold is currently on 5 matches

The team–match linking logic is separated into three distinct cases:

- If a team plays six or more matches from its first match in the tournament to its last match in that tournament
  
  - Take the statistics for that period
 
- If it is the team's first match in the tournament

  - Take the statistics from previous tournament

- If a team plays less than six matches from its first match in the tournament to its last match in that tournament

  - Take the statistics from the previous tournament, reduced to five games
 
  - Combine the reduced statistics from the previous tournament with data from the period between the first and last games in the current tournament

<img src="pictures/team_match_linking.png" width="1200">

## Improving Consistency and Model Generalization

- Create difference and ratio features from the team's data, then remove the individual team columns.
  This encourages the model to learn from the differences between teams rather than individual team stats, so it does not matter which team is labeled A or B.
   
- Generate mirror matches to improve generalization (only train set).
  For most of the data, it does not matter whether a team is listed first or second (this is what I aimed to achieve).
  
## Data Dynamics and Time-Based Weighting

League of Legends is a highly dynamic game with monthly patches and meta shifts. To ensure the model reflects the current state of the game, the training process incorporates the following temporal strategies:

- Validation Set Selection: The validation set always consists of the most recent data (the last 2 months of matches). This ensures that hyperparameter tuning is optimized for the latest game version and team compositions.

- Time-Based Sample Weighting: A linear scaling function is applied to the training data to prioritize newer matches.

     - The oldest match in the training set is assigned a weight of 0.

     - The most recent match in the training set is assigned a weight of 1.

     - All other matches are assigned weights on a continuous scale between 0 and 1 based on their date.

- Adaptive Training: By using these weights during the training phase, the model learns more from recent performance trends while still retaining long-term historical context.



## how to use it (Linux)

- Clone the repository

  ```bash
  git clone https://github.com/pavlila/lol-intra-league-predictor.git

  cd lol-intra-league-predictor

- Sync the environment

  ```bash
  uv sync

- Running the Application

  ```bash
  uv run streamlit run app.py

At the bottom of the application, I prepare the most recent matches from each league in the 2025 season to simulate realistic predictions.

## Validation accuracy

The percentages represent the accuracy of each model. The model with the highest accuracy is selected as the final predictor.
- Decision Tree: 69.23%
- AdaBoost: 70.85%
- Random Forest: 72.46%
- XGBoost: 70.04%
- Logistic Regression: 71.25%


## Testing accuracy

Evaluation Challenges: Achieving an objective accuracy metric is challenging in the context of League of Legends. Given the high variance between patches and player behavior, a realistic evaluation requires a long-term observation period (minimum 2 months) in a live environment to account for meta shifts and ensure the model's robustness.
