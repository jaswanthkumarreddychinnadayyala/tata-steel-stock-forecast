# Tata Steel Stock Forecasting

A robust machine learning pipeline for forecasting Tata Steel stock prices using historical market data, featuring XGBoost regression, comprehensive feature engineering, and SHAP explainability.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Project Goal

Reliably forecast Tata Steel stock prices using historical market data to help investors and planners manage risk and make better decisions. The solution focuses on:
- **Accuracy**: Robust predictive performance
- **Reliability**: Protection against look-ahead bias and data leakage
- **Explainability**: Actionable insights via SHAP values
- **Robustness**: Handles market regime shifts and noisy data

## 📁 Project Structure

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
├── predict.py           # Prediction script for new data
├── setup.py             # Package installation
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── PROJECT_OVERVIEW.md  # Detailed technical documentation
└── LICENSE              # MIT License
```

## 🚀 Quick Start

### 1. Installation

```powershell
# Clone the repository
git clone https://github.com/<your-username>/tata-steel-forecast.git
cd tata-steel-forecast

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Train a Model

```powershell
python train.py --data data/sample_data.csv --target Close --date_col Date
```

### 3. Make Predictions

```powershell
python predict.py --model models/xgb_model.joblib --data data/sample_data.csv --output predictions.csv
```

### 4. Run Tests

```powershell
pytest tests/ -v
```

## 🔧 What's Included

### Feature Engineering
- **Lagged prices**: Close prices from 1, 2, 3, and 5 days ago
- **Returns**: Daily percentage changes
- **Rolling statistics**: 5, 10, 20-day moving averages and volatility
- **Momentum indicators**: Price ratios over different windows
- **Calendar effects**: Day of week, month
- **Strict lagging**: All features prevent look-ahead bias

### Model Pipeline
- **Algorithm**: XGBoost regressor with early stopping
- **Validation**: TimeSeriesSplit (5 folds) for time-aware cross-validation
- **Metrics**: RMSE and MAE for performance evaluation
- **Selection**: Best model chosen by lowest validation RMSE

### Explainability
- **SHAP values**: Feature importance analysis
- **Actionable insights**: Understand what drives predictions

## 📊 Usage Examples

### Training Arguments

```powershell
python train.py --help

Options:
  --data TEXT        Path to CSV data file (required)
  --date_col TEXT    Date column name (default: "Date")
  --target TEXT      Target column name (default: "Close")
  --out_dir TEXT     Output directory for models (default: "models")
```

### Expected CSV Format

Your data file should have at minimum:
```csv
Date,Close
2020-01-01,100
2020-01-02,101
...
```

Additional columns like Open, High, Low, Volume are optional but can be used as features.

### Prediction Output

The `predict.py` script generates a CSV with forecasted next-day close prices:
```csv
Date,predicted_next_day_close
2020-01-15,110.5
2020-01-16,111.2
...
```

## 🎓 Technical Approach

### Challenges Addressed
1. **Feature Leakage**: Strict lagging ensures no future information in training
2. **Look-Ahead Bias**: TimeSeriesSplit validates on future data only
3. **Non-Stationary Signals**: Rolling statistics capture regime changes
4. **Overfitting**: Cross-validation and early stopping prevent overfit
5. **Outliers**: Robust features handle market volatility

### Model Performance
- Evaluation uses **RMSE** and **MAE** metrics
- TimeSeriesSplit provides realistic out-of-sample performance
- Best fold model selected for deployment
- Metrics saved to `models/metrics.json`

## 🔮 Future Enhancements

- [ ] **Deep Learning**: LSTM, GRU, or Temporal Fusion Transformers
- [ ] **Probabilistic Forecasting**: Prediction intervals and uncertainty quantification
- [ ] **Hyperparameter Tuning**: Optuna or GridSearchCV optimization
- [ ] **Live Data**: Integration with real-time market data APIs
- [ ] **MLOps**: Model versioning, monitoring, and automated retraining
- [ ] **Model Comparison**: Random Forest, LightGBM, CatBoost benchmarks
- [ ] **Walk-Forward**: More rigorous out-of-sample validation

## 📤 Push to GitHub

1. Create a new repository on GitHub (e.g., `tata-steel-forecast`)
2. Run these commands from your project folder:

```powershell
git init
git add .
git commit -m "Initial commit: Stock forecasting pipeline"
git branch -M main
git remote add origin https://github.com/<your-username>/tata-steel-forecast.git
git push -u origin main
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

For questions, issues, or collaboration:
- Open an issue on GitHub
- Check [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for detailed documentation

## ⚠️ Disclaimer

This model is for **educational and research purposes only**. Always conduct thorough due diligence and consult with financial advisors before making investment decisions. Past performance does not guarantee future results.

---

**Built with ❤️ for reliable stock price forecasting**
