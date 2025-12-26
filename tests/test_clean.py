import pytest
import pandas as pd
import numpy as np
from pathlib import Path

def test_compare_csv_outputs_teams():
    TEST_DIR = Path(__file__).parent
    expected = pd.read_csv(TEST_DIR / 'test_clean_data_teams.csv')
    actual_2023 = pd.read_csv(TEST_DIR.parent / 'data/cleaned/teams/2023.csv')
    actual_2024 = pd.read_csv(TEST_DIR.parent / 'data/cleaned/teams/2024.csv')
    actual_2025 = pd.read_csv(TEST_DIR.parent / 'data/cleaned/teams/2025.csv')
    actual = pd.concat([actual_2023, actual_2024, actual_2025], ignore_index=True)
    actual['date'] = pd.to_datetime(actual['date'])
    expected['date'] = pd.to_datetime(expected['date'])

    comparison = expected[['Team','date','split','playoffs']].merge(actual, on=['Team','date','split','playoffs'], how='inner')

    assert len(comparison) == len(expected), "Mismatch in number of rows between expected and actual data."

    expected = expected.sort_values(['Team','date']).reset_index(drop=True)
    comparison = comparison.sort_values(['Team','date']).reset_index(drop=True)

    cols_to_test = [c for c in expected.columns if c not in ['Team', 'date', 'tournament', 'split', 'playoffs']]

    for col in cols_to_test:
        actual_values = pd.to_numeric(comparison[col], errors='coerce').fillna(0).values
        expected_values = pd.to_numeric(expected[col], errors='coerce').fillna(0).values

        np.testing.assert_allclose(actual_values, expected_values, rtol=0.05, atol=0.01, err_msg=f"Mismatch found in column: {col}")

def test_compare_csv_outputs_matches():
    TEST_DIR = Path(__file__).parent
    expected = pd.read_csv(TEST_DIR / 'test_clean_data_matches.csv')
    actual_2023 = pd.read_csv(TEST_DIR.parent / 'data/cleaned/matches/2023.csv')
    actual_2024 = pd.read_csv(TEST_DIR.parent / 'data/cleaned/matches/2024.csv')
    actual_2025 = pd.read_csv(TEST_DIR.parent / 'data/cleaned/matches/2025.csv')
    actual = pd.concat([actual_2023, actual_2024, actual_2025], ignore_index=True)
    actual['date'] = pd.to_datetime(actual['date'])
    expected['date'] = pd.to_datetime(expected['date'])

    comparison = expected[['teamA','teamB','date','teamA_win']].merge(actual, on=['teamA','teamB','date','teamA_win'], how='inner')

    assert len(comparison) == len(expected), "Mismatch in number of rows between expected and actual data."

    expected = expected.sort_values(['teamA','teamB','date']).reset_index(drop=True)
    comparison = comparison.sort_values(['teamA','teamB','date']).reset_index(drop=True)

    cols_to_test = [c for c in expected.columns if c not in ['league', 'split', 'playoffs']]

    for col in cols_to_test:
        actual_values = pd.to_numeric(comparison[col], errors='coerce').fillna(0).values
        expected_values = pd.to_numeric(expected[col], errors='coerce').fillna(0).values

        np.testing.assert_allclose(actual_values, expected_values, rtol=0.05, atol=0.01, err_msg=f"Mismatch found in column: {col}")

if __name__ == "__main__":
    pytest.main([__file__])
