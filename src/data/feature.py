import pandas as pd

def makeMirror(df):
    """Rozmnoží dataset: každý zápas A vs B dostane i zrcadlenou verzi B vs A."""

    # Kopie původního dataframe
    df_orig = df.copy()

    # Mirror = prohodíme všechny A/B sloupce
    df_mirror = df.copy()
    
    a_cols = [c for c in df.columns if c.endswith('_A')]
    for a_col in a_cols:
        base = a_col[:-2]
        b_col = f"{base}_B"
        df_mirror[a_col], df_mirror[b_col] = df[b_col], df[a_col]

    # Prohodíme i názvy týmů
    df_mirror['teamA'], df_mirror['teamB'] = df['teamB'], df['teamA']

    # Label musíme zrcadlit → pokud vyhrál A v originálu, v mirroru vyhrál B
    df_mirror['teamA_win'] = 1 - df['teamA_win']

    # Spojíme originál + mirror
    df_out = pd.concat([df_orig, df_mirror], ignore_index=True)

    return df_out
    
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


def makeFeature(df, month_validation=1):
    df['date'] = pd.to_datetime(df['date'])

    max_date = df['date'].max()
    validation_start = max_date - pd.DateOffset(months=month_validation)

    train_df = df[df['date'] < validation_start].copy()
    val_df = df[df['date'] >= validation_start].copy()

    train_df = makeMirror(train_df)

    meta_cols = ['teamA', 'teamB', 'league']
    
    train_df = makeDiff(train_df.drop(columns=meta_cols, errors='ignore'))
    val_df = makeDiff(val_df.drop(columns=meta_cols, errors='ignore'))

    train_df = train_df.fillna(-1)
    val_df = val_df.fillna(-1)

    return train_df, val_df

data = pd.read_csv("../../data/merged/data.csv", sep=',')

train_df, val_df = makeFeature(data, month_validation=2)
train_df.to_csv("../../data/featured/train.csv", sep=',', index=False)
val_df.to_csv("../../data/featured/val.csv", sep=',', index=False)