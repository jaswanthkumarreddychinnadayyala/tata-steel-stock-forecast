import argparse
import os
import pandas as pd
from src.model import load_model
from src.data import load_data, prepare_features


def predict(model_path: str, data_path: str, date_col: str = "Date", target_col: str = "Close"):
    """Load model and make predictions on new data."""
    model = load_model(model_path)
    df = load_data(data_path, date_col=date_col)
    dfp = prepare_features(df, target_col=target_col, date_col=date_col, dropna=False)
    
    # Get features (same as training)
    import numpy as np
    features = [c for c in dfp.columns if c not in [date_col, "target"]]
    X = dfp[features].select_dtypes(include=[np.number])
    
    # Remove rows with NaN (initial rows due to lagging)
    valid_idx = X.notna().all(axis=1)
    X_valid = X[valid_idx]
    dates_valid = dfp[date_col][valid_idx]
    
    # Predict
    predictions = model.predict(X_valid)
    
    # Create results dataframe
    results = pd.DataFrame({
        date_col: dates_valid.values,
        "predicted_next_day_close": predictions
    })
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Make predictions using trained model")
    parser.add_argument("--model", required=True, help="Path to trained model (.joblib)")
    parser.add_argument("--data", required=True, help="Path to CSV data")
    parser.add_argument("--date_col", default="Date")
    parser.add_argument("--target", default="Close")
    parser.add_argument("--output", default="predictions.csv", help="Output CSV file")
    args = parser.parse_args()
    
    if not os.path.exists(args.model):
        print(f"Error: Model file not found: {args.model}")
        return
    
    if not os.path.exists(args.data):
        print(f"Error: Data file not found: {args.data}")
        return
    
    results = predict(args.model, args.data, args.date_col, args.target)
    results.to_csv(args.output, index=False)
    print(f"Predictions saved to {args.output}")
    print(f"\nFirst 5 predictions:")
    print(results.head())
    print(f"\nLast 5 predictions:")
    print(results.tail())


if __name__ == "__main__":
    main()
