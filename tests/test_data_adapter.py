import pandas as pd

from src.data_adapter import (
    normalize_column_name,
    clean_numeric,
    prepare_customer_data
)


def test_normalize_column_name():
    assert normalize_column_name("Annual Income (₹)") == "annual_income"
    assert normalize_column_name("Purchase Frequency") == "purchase_frequency"


def test_clean_numeric():
    data = pd.Series(["₹82,468", "$50,000", "82.5"])

    result = clean_numeric(data)

    assert result.iloc[0] == 82468
    assert result.iloc[1] == 50000
    assert result.iloc[2] == 82.5


def test_prepare_customer_data():
    df = pd.DataFrame({
        "Age": [25, 35],
        "Annual Income": [500000, 800000],
        "Purchase Frequency": [5, 10],
        "Annual Spending": [50000, 120000]
    })

    result, mapping, missing = prepare_customer_data(df)

    assert result is not None
    assert list(result.columns) == [
        "age",
        "income",
        "purchase_frequency",
        "annual_spending"
    ]
    assert len(result) == 2
    assert missing == []


def test_income_lpa_conversion():
    df = pd.DataFrame({
        "Age": [25],
        "Income LPA": [8],
        "Purchase Frequency": [5],
        "Annual Spending": [100000]
    })

    result, mapping, missing = prepare_customer_data(df)

    assert result["income"].iloc[0] == 800000
    assert missing == []


def test_monthly_income_conversion():
    df = pd.DataFrame({
        "Age": [25],
        "Monthly Income": [50000],
        "Purchase Frequency": [5],
        "Annual Spending": [100000]
    })

    result, mapping, missing = prepare_customer_data(df)

    assert result["income"].iloc[0] == 600000
    assert missing == []


def test_missing_required_columns():
    df = pd.DataFrame({
        "Age": [25],
        "Annual Income": [500000]
    })

    result, mapping, missing = prepare_customer_data(df)

    assert result is None
    assert len(missing) > 0