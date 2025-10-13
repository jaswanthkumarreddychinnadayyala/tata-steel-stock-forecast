import os
import sys
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data import load_data, prepare_features

# Try to import model functions
try:
    from src.model import train_xgb, save_model, load_model
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


def test_pipeline_runs():
    """Test that the full pipeline runs end-to-end."""
    if not XGBOOST_AVAILABLE:
        import pytest
        pytest.skip("XGBoost not available")
    
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.csv")
    df = load_data(data_path)
    dfp = prepare_features(df)
    features = [c for c in dfp.columns if c not in ["Date", "target"]]
    X = dfp[features].select_dtypes(include=[np.number])
    y = dfp["target"]
    
    # Train with fewer splits for faster testing
    model, summary = train_xgb(X, y, n_splits=2)
    
    assert "mean_rmse" in summary
    assert "mean_mae" in summary
    assert summary["mean_rmse"] > 0
    assert summary["mean_mae"] > 0
    assert X.shape[0] > 0
    assert len(y) == X.shape[0]


def test_model_save_load():
    """Test model saving and loading."""
    if not XGBOOST_AVAILABLE:
        import pytest
        pytest.skip("XGBoost not available")
    
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.csv")
    df = load_data(data_path)
    dfp = prepare_features(df)
    features = [c for c in dfp.columns if c not in ["Date", "target"]]
    X = dfp[features].select_dtypes(include=[np.number])
    y = dfp["target"]
    
    # Train model
    model, _ = train_xgb(X, y, n_splits=2)
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), "test_model.joblib")
    save_model(model, model_path)
    assert os.path.exists(model_path)
    
    # Load model
    loaded_model = load_model(model_path)
    
    # Test predictions match
    pred1 = model.predict(X)
    pred2 = loaded_model.predict(X)
    assert np.allclose(pred1, pred2)
    
    # Cleanup
    if os.path.exists(model_path):
        os.remove(model_path)


def test_predictions_reasonable():
    """Test that predictions are in a reasonable range."""
    if not XGBOOST_AVAILABLE:
        import pytest
        pytest.skip("XGBoost not available")
    
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.csv")
    df = load_data(data_path)
    dfp = prepare_features(df)
    features = [c for c in dfp.columns if c not in ["Date", "target"]]
    X = dfp[features].select_dtypes(include=[np.number])
    y = dfp["target"]
    
    model, _ = train_xgb(X, y, n_splits=2)
    predictions = model.predict(X)
    
    # Predictions should be close to actual values
    assert predictions.min() > 0  # Prices should be positive
    assert np.abs(predictions.mean() - y.mean()) < y.std() * 2  # Reasonable range
