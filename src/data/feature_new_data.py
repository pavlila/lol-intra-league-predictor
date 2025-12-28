import pandas as pd
import numpy as np

def makeDiff(df):
    a_cols = [c for c in df.columns if c.endswith('_A')]
    diff_data = {}
    ratio_data = {}

    for a_col in a_cols:
        base = a_col[:-2]
        b_col = f"{base}_B"
        if b_col in df.columns:
            diff_data[f'diff_{base}'] = df[a_col] - df[b_col]
            ratio_data[f'ratio_{base}'] = df[a_col] / (df[b_col] + 1e-6)

    df = pd.concat([df, pd.DataFrame(diff_data), pd.DataFrame(ratio_data)], axis=1)
    drop_cols = [c for c in df.columns if c.endswith('_A') or c.endswith('_B')]
    df = df.drop(columns=drop_cols)
    return df


def makeFeature(df):
    df['date'] = pd.to_datetime(df['date'])

    max_date = df['date'].max()

    meta_cols = ['teamA', 'teamB', 'league']
    
    df = makeDiff(df.drop(columns=meta_cols, errors='ignore'))

    return df