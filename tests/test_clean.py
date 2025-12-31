import pytest
import pandas as pd
import numpy as np
from pathlib import Path


def test_compare_csv_outputs_teams():
    """
    Compares the processed team data with reference datasets to ensure accuracy.

    Validates that statistical columns in 'teams.csv' align with expected values
    from the reference file. The test checks for row consistency and uses
    defined tolerances (5% relative, 0.01 absolute) for numeric comparisons.
    """
    TEST_DIR = Path(__file__).parent
    expected = pd.read_csv(TEST_DIR / "test_clean_data_teams.csv")
    data = pd.read_csv(TEST_DIR.parent / "data" / "cleaned" / "teams.csv")
    data["date"] = pd.to_datetime(data["date"])
    expected["date"] = pd.to_datetime(expected["date"])

    comparison = expected[["Team", "date", "league"]].merge(
        data, on=["Team", "date", "league"], how="inner"
    )

    assert len(comparison) == len(
        expected
    ), "Mismatch in number of rows between expected and actual data."

    expected = expected.sort_values(["Team", "date", "league"]).reset_index(drop=True)
    comparison = comparison.sort_values(["Team", "date", "league"]).reset_index(
        drop=True
    )

    cols_to_test = [c for c in expected.columns if c not in ["Team", "date", "league"]]

    for col in cols_to_test:
        actual_values = pd.to_numeric(comparison[col], errors="coerce").fillna(0).values
        expected_values = pd.to_numeric(expected[col], errors="coerce").fillna(0).values

        np.testing.assert_allclose(
            actual_values,
            expected_values,
            rtol=0.05,
            atol=0.01,
            err_msg=f"Mismatch found in column: {col}",
        )


if __name__ == "__main__":
    pytest.main([__file__])
