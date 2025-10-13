import os
from src.data import load_data, prepare_features
from src.model import train_xgb


def test_pipeline_runs():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.csv")
    df = load_data(data_path)
    dfp = prepare_features(df)
    features = [c for c in dfp.columns if c not in ["Date", "target"]]
    X = dfp[features]
    y = dfp["target"]
    model, summary = train_xgb(X, y, n_splits=2)
    assert "mean_rmse" in summary
    assert X.shape[0] > 0
