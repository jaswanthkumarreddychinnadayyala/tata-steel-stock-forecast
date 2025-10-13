import pandas as pd
import numpy as np
from typing import List


def load_data(path: str, date_col: str = "Date") -> pd.DataFrame:
    df = pd.read_csv(path)
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)
    return df


def add_lag_features(
    df: pd.DataFrame,
    target_col: str = "Close",
    lags: List[int] = [1, 2, 3],
) -> pd.DataFrame:
    df = df.copy()
    for lag in lags:
        df[f"{target_col}_lag_{lag}"] = df[target_col].shift(lag)
    return df


def add_return_and_rolling(
    df: pd.DataFrame,
    target_col: str = "Close",
    date_col: str = "Date",
    returns_lags: List[int] = [1],
    rolling_windows: List[int] = [5, 10, 20],
) -> pd.DataFrame:
    df = df.copy()
    # returns
    df["return_1"] = df[target_col].pct_change()
    for lag in returns_lags:
        df[f"return_{lag}_lag"] = df["return_1"].shift(lag)
    # rolling mean and std (lagged)
    for w in rolling_windows:
        df[f"roll_mean_{w}"] = df[target_col].rolling(window=w).mean().shift(1)
        df[f"roll_std_{w}"] = df[target_col].rolling(window=w).std().shift(1)
    # momentum: close / close_{n_days_ago} - 1
    for w in rolling_windows:
        df[f"mom_{w}"] = df[target_col] / df[target_col].shift(w) - 1
    # calendar features
    if date_col in df.columns:
        df["day_of_week"] = df[date_col].dt.dayofweek
        df["month"] = df[date_col].dt.month
    return df


def prepare_features(
    df: pd.DataFrame,
    target_col: str = "Close",
    date_col: str = "Date",
    dropna: bool = True,
) -> pd.DataFrame:
    df = df.copy()
    df = add_lag_features(df, target_col=target_col, lags=[1,2,3,5])
    df = add_return_and_rolling(df, target_col=target_col, date_col=date_col, returns_lags=[1], rolling_windows=[5,10,20])
    # target: next-day return or next-day price
    df["target"] = df[target_col].shift(-1)
    if dropna:
        df = df.dropna().reset_index(drop=True)
    return df
