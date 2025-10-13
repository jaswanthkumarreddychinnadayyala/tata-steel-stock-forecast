import argparse
import os
import json
import numpy as np
from src.data import load_data, prepare_features
from src.model import train_xgb, save_model, explain_model


def main():
    parser = argparse.ArgumentParser(description="Train XGBoost on stock data")
    parser.add_argument("--data", required=True, help="Path to CSV data")
    parser.add_argument("--date_col", default="Date")
    parser.add_argument("--target", default="Close")
    parser.add_argument("--out_dir", default="models")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    df = load_data(args.data, date_col=args.date_col)
    dfp = prepare_features(df, target_col=args.target, date_col=args.date_col)
    # exclude date column and the target column
    features = [c for c in dfp.columns if c not in [args.date_col, "target"]]
    X = dfp[features].select_dtypes(include=[np.number])
    y = dfp["target"]
    model, summary = train_xgb(X, y)
    model_path = os.path.join(args.out_dir, "xgb_model.joblib")
    save_model(model, model_path)
    # save metrics
    metrics_path = os.path.join(args.out_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(summary, f, indent=2)
    print("Training summary:", summary)
    # explain top features on last 100 rows
    shap_df = explain_model(model, X.tail(100))
    if shap_df is not None:
        print("Top SHAP features:\n", shap_df)
    else:
        print("SHAP is not available or failed to run; install shap to enable explainability.")


if __name__ == "__main__":
    main()
