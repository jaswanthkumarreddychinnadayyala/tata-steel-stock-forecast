# Models Directory

This directory will contain trained models and evaluation metrics.

## Generated Files

After running `train.py`, you'll find:
- `xgb_model.joblib` - Trained XGBoost model
- `metrics.json` - Training metrics (RMSE, MAE)

## Usage

Load a model in Python:
```python
from src.model import load_model

model = load_model("models/xgb_model.joblib")
predictions = model.predict(X_test)
```

## Note

This directory is in `.gitignore` to prevent committing large model files.
For production, consider using:
- Git LFS for model versioning
- MLflow for model registry
- DVC for data/model versioning
