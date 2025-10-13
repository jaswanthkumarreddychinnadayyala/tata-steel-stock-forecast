# Tata Steel Stock Forecasting Project

## Overview
This project implements a robust machine learning pipeline for forecasting Tata Steel stock prices using historical market data. The solution focuses on accuracy, robustness against market regime shifts, and explainability.

## Key Features
- **Feature Engineering**: Lagged returns, rolling statistics (mean/volatility), momentum factors, and calendar effects
- **Time-Aware Validation**: TimeSeriesSplit to avoid look-ahead bias and data leakage
- **Model Training**: XGBoost regressor with hyperparameter tuning
- **Evaluation Metrics**: RMSE and MAE for model performance
- **Explainability**: SHAP values for feature importance and investment insights

## Project Structure
```
stocks/
├── src/
│   ├── __init__.py
│   ├── data.py          # Data loading and feature engineering
│   └── model.py         # Model training, evaluation, and explainability
├── data/
│   └── sample_data.csv  # Sample dataset for testing
├── models/              # Trained models and metrics (generated)
├── tests/
│   └── test_pipeline.py # Unit tests
├── train.py             # Main training script
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. Clone this repository:
```powershell
git clone https://github.com/<your-username>/tata-steel-forecast.git
cd tata-steel-forecast
```

2. Create a virtual environment (recommended):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

## Usage

### Training a Model
Run the training script with your dataset:

```powershell
python train.py --data data/sample_data.csv --target Close --date_col Date
```

**Arguments:**
- `--data`: Path to CSV file with historical stock data (required)
- `--target`: Name of the target column (default: "Close")
- `--date_col`: Name of the date column (default: "Date")
- `--out_dir`: Directory to save model and metrics (default: "models")

**Expected CSV Format:**
```csv
Date,Open,High,Low,Close,Volume
2020-01-01,100,101,99,100,1000
2020-01-02,100,102,98,101,1100
...
```

### Output
The training script will:
1. Generate engineered features (lags, rolling stats, momentum)
2. Train an XGBoost model using TimeSeriesSplit cross-validation
3. Save the best model to `models/xgb_model.joblib`
4. Save metrics (RMSE, MAE) to `models/metrics.json`
5. Display top SHAP feature importances

### Running Tests
```powershell
pytest tests/ -v
```

## Technical Approach

### Feature Engineering
All features are **strictly lagged** to prevent look-ahead bias:
- **Lagged prices**: Close prices from 1, 2, 3, and 5 days ago
- **Returns**: Daily percentage changes
- **Rolling statistics**: 5, 10, 20-day moving averages and standard deviations
- **Momentum**: Price ratios over different windows
- **Calendar features**: Day of week, month

### Model Training
- **Algorithm**: XGBoost regressor
- **Validation**: TimeSeriesSplit (5 folds by default)
- **Metrics**: RMSE and MAE
- **Selection**: Best fold model based on lowest RMSE

### Explainability
- SHAP (SHapley Additive exPlanations) values for feature importance
- Identifies which features drive predictions
- Provides actionable insights for investment decisions

## Challenges Addressed
1. **Feature Leakage**: Strict lagging ensures no future data in features
2. **Non-Stationary Signals**: Rolling statistics capture regime changes
3. **Overfitting**: Time-aware cross-validation prevents data leakage
4. **Outliers**: Robust feature engineering handles market volatility

## Future Improvements
- [ ] Sequence models (LSTM, Temporal Fusion Transformers)
- [ ] Probabilistic forecasting (prediction intervals)
- [ ] Hyperparameter tuning with Optuna
- [ ] Live data integration via APIs
- [ ] MLOps pipeline (model versioning, monitoring, retraining)
- [ ] Model comparison framework
- [ ] Walk-forward optimization

## Results and Impact
- Reliable short-term forecasts for scenario analysis
- Actionable feature importances for investment insights
- Robust performance across different market conditions
- Foundation for automated trading strategies

## License
MIT License

## Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## Contact
For questions or collaboration, please open an issue on GitHub.

---

**Note**: This model is for educational and research purposes. Always conduct thorough due diligence before making investment decisions.
