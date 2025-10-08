# lol-worlds-2025-predict

This project predicts the outcomes of League of Legends matches within individual leagues using match data from [gol.gg](https://gol.gg/) and team statistics from [oracleselixir.com](https://oracleselixir.com/). 
It focuses exclusively on intra-league predictions. 
The model dynamically adapts to the most up-to-date team statistics and performance within each tournament.

## Used tournaments

$(YEARS) = {
        2025
        }

- LPL

        LPL $YEARS Split 1 

        LPL $YEARS Split 1 Playoffs

        LPL $YEARS Split 2 Placements

        LPL $YEARS Split 2

        LPL $YEARS Split 2 Playoffs

        LPL $YEARS Split 3

- LEC

        LEC $YEARS Winter

        LEC $YEARS Winter Playoffs

        LEC $YEARS Spring Season

        LEC $YEARS Spring Playoffs

        LEC $YEARS Summer Season

- LCK

        LCK $YEARS Cup

        LCK $YEARS Rounds 1-2

        LCK $YEARS Road to MSI

        LCK $YEARS Rounds 3-5

- LTA N

        LTA North $YEARS Split 1

        LTA North $YEARS Split 2

        LTA North $YEARS Split 2 Playoffs

        LTA North $YEARS Split 3

- LTA S

        LTA South $YEARS Split 1

        LTA South $YEARS Split 2

        LTA South $YEARS Split 2 Playoffs

        LTA South $YEARS Split 3

- LCP

        LCP $YEARS Season Kickoff

        LCP $YEARS Season Kickoff Qualifying Series

        LCP $YEARS Mid Season

        LCP $YEARS Mid Season Qualifying Series

        LCP $YEARS Season Finals


## About data

  - All the data presented below comes after the data cleaning phase

     - Matches data
   
           tournament: Tournament Name

           date: Date of the Match

           teamA: Name of the First Team

           teamB: Name of the Second Team

           teamA_win: Binary outcome - 1 if the first team wins, 0 if the second team wins

     - Teams data
   
           tournament: Tournament Name

           date: Date on which the statistic was recorded (aggregated from the start of the tournament up to this date

           Team: Team Name

           GP: Games Played

           AGT: Average game time/duration, in minutes

           KD: Kill-to-Death Ratio

           CKPM: Average combined kills per minute (team kills + opponent kills)

           GPR: Gold percent rating (average amount of game's total gold held, relative to 50%)

           GSPD: Average gold spent percentage difference

           EGR: Early-Game Rating

           MLR: Mid/Late Rating

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

               - The raw statistics for Wins (W) and Losses (L) were removed after computing the win rate percentage (winrate%)

## Team-Match Linking Logic

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
   
- Generate mirror matches to improve generalization.
  For most of the data, it does not matter whether a team is listed first or second (this is what I aimed to achieve).

## how to use it (Linux)

TO DO


## Validation accuracy

The percentages represent the model’s predicted probabilities of each outcome, and the data is split into 50% training and 30% validation sets with a random seed of 42.

- Decision Tree: x/y z%
- Random Forest: x/y z%
- XGBoost: x/y z%
- Logistic Regression: x/y z%

## Testing accuracy

The validation and test sets are combined into a single.
Test set representing 20% of the total dataset.

- Decision Tree: x/y z%
- Random Forest: x/y z%
- XGBoost: x/y z%
- Logistic Regression: x/y z%
