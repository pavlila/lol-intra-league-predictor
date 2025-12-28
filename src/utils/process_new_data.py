from clean_new_data import newMatchesCleanByMatch
import pandas as pd
from feature_new_data import makeFeature
from merge_new_data import mergeNewDataWithTeamsData

def processNewData(df):
    cleaned_df = newMatchesCleanByMatch(df)

    teams_data = pd.read_csv("../../data/merged/data.csv", sep=',')

    merged_df = mergeNewDataWithTeamsData(cleaned_df, teams_data)

    featured_df = makeFeature(merged_df)

    return featured_df
