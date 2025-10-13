import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
from typing import Tuple, Dict, Optional, Any


def train_xgb(
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
    params: dict = None,
) -> Tuple[Any, Dict]:
    if params is None:
        params = {"n_estimators": 100, "max_depth": 4, "learning_rate": 0.05}
    tscv = TimeSeriesSplit(n_splits=n_splits)
    fold = 0
    metrics = {"rmse": [], "mae": []}
    models = []
    for train_idx, val_idx in tscv.split(X):
        fold += 1
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        # lazy import xgboost to avoid import errors if package missing
        try:
            import xgboost as xgb
        except Exception as e:
            raise RuntimeError("xgboost is required to train the model. Install it with `pip install xgboost`. Error: {}".format(e))
        model = xgb.XGBRegressor(**params, early_stopping_rounds=10)
        model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
        preds = model.predict(X_val)
        mse = mean_squared_error(y_val, preds)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_val, preds)
        metrics["rmse"].append(rmse)
        metrics["mae"].append(mae)
        models.append(model)
    # choose best model by average RMSE
    best_idx = int(np.argmin(metrics["rmse"]))
    best_model = models[best_idx]
    summary = {"mean_rmse": float(np.mean(metrics["rmse"])), "mean_mae": float(np.mean(metrics["mae"]))}
    return best_model, summary


def explain_model(model, X_sample: pd.DataFrame, max_display: int = 10) -> Optional[pd.DataFrame]:
    # shap can be heavy or missing; import lazily and fail gracefully
    try:
        import shap
    except Exception:
        return None
    try:
        explainer = shap.Explainer(model)
        shap_values = explainer(X_sample)
        # return top features by mean absolute SHAP
        shap_df = pd.DataFrame({
            "feature": X_sample.columns,
            "mean_abs_shap": np.abs(shap_values.values).mean(axis=0),
        })
        shap_df = shap_df.sort_values("mean_abs_shap", ascending=False).head(max_display)
        return shap_df
    except Exception:
        return None


def save_model(model, path: str):
    joblib.dump(model, path)


def load_model(path: str):
    return joblib.load(path)
