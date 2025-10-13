import os
import sys
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data import load_data, add_lag_features, add_return_and_rolling, prepare_features


def test_load_data():
    """Test data loading function."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.csv")
    df = load_data(data_path)
    assert isinstance(df, pd.DataFrame)
    assert "Date" in df.columns
    assert "Close" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])


def test_add_lag_features():
    """Test lag feature creation."""
    df = pd.DataFrame({"Close": [100, 101, 102, 103, 104]})
    df_lagged = add_lag_features(df, target_col="Close", lags=[1, 2])
    assert "Close_lag_1" in df_lagged.columns
    assert "Close_lag_2" in df_lagged.columns
    assert df_lagged["Close_lag_1"].iloc[1] == 100
    assert df_lagged["Close_lag_2"].iloc[2] == 100


def test_add_return_and_rolling():
    """Test return and rolling feature creation."""
    df = pd.DataFrame({
        "Date": pd.date_range("2020-01-01", periods=30),
        "Close": np.linspace(100, 130, 30)
    })
    df_features = add_return_and_rolling(df, target_col="Close", date_col="Date", rolling_windows=[5, 10])
    assert "return_1" in df_features.columns
    assert "roll_mean_5" in df_features.columns
    assert "roll_std_5" in df_features.columns
    assert "mom_5" in df_features.columns
    assert "day_of_week" in df_features.columns
    assert "month" in df_features.columns


def test_prepare_features():
    """Test full feature preparation pipeline."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.csv")
    df = load_data(data_path)
    dfp = prepare_features(df, target_col="Close", date_col="Date")
    
    # Check that features were created
    assert "Close_lag_1" in dfp.columns
    assert "return_1_lag" in dfp.columns
    assert "roll_mean_5" in dfp.columns
    assert "target" in dfp.columns
    
    # Check no NaN after dropna
    assert dfp.isna().sum().sum() == 0
    
    # Check target is correctly shifted
    assert len(dfp) > 0


def test_feature_no_leakage():
    """Test that features don't use future information."""
    df = pd.DataFrame({
        "Date": pd.date_range("2020-01-01", periods=10),
        "Close": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    })
    dfp = prepare_features(df, target_col="Close", date_col="Date", dropna=False)
    
    # Lag features should be NaN in first rows
    assert pd.isna(dfp["Close_lag_1"].iloc[0])
    
    # Rolling features should be NaN in early rows
    assert pd.isna(dfp["roll_mean_5"].iloc[0])
    
    # Target should be next day's close
    assert dfp["target"].iloc[0] == 101
