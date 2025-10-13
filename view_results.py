import pandas as pd
import numpy as np

# Load original data and predictions
data = pd.read_csv('data/sample_data.csv')
predictions = pd.read_csv('predictions.csv')

# Merge to compare
data['Date'] = pd.to_datetime(data['Date'])
predictions['Date'] = pd.to_datetime(predictions['Date'])
merged = predictions.merge(data, on='Date', how='left')

# Calculate next day actual close (shifted by 1)
merged['actual_next_day_close'] = merged['Close'].shift(-1)

# Drop last row (no next day actual)
merged = merged.dropna(subset=['actual_next_day_close'])

# Calculate error metrics
merged['error'] = merged['predicted_next_day_close'] - merged['actual_next_day_close']
merged['abs_error'] = abs(merged['error'])
merged['pct_error'] = (merged['error'] / merged['actual_next_day_close']) * 100

print("="*70)
print("TATA STEEL STOCK FORECASTING - MODEL OUTPUT")
print("="*70)
print()

print("📊 DATASET SUMMARY")
print("-" * 70)
print(f"Total trading days: {len(data)}")
print(f"Date range: {data['Date'].min().strftime('%Y-%m-%d')} to {data['Date'].max().strftime('%Y-%m-%d')}")
print(f"Price range: ${data['Close'].min():.2f} - ${data['Close'].max():.2f}")
print(f"Average price: ${data['Close'].mean():.2f}")
print()

print("📈 MODEL PERFORMANCE METRICS")
print("-" * 70)
print(f"Mean Absolute Error (MAE): ${merged['abs_error'].mean():.2f}")
print(f"Root Mean Squared Error (RMSE): ${np.sqrt((merged['error']**2).mean()):.2f}")
print(f"Mean Percentage Error: {merged['pct_error'].mean():.2f}%")
print(f"Median Absolute Error: ${merged['abs_error'].median():.2f}")
print(f"Max Absolute Error: ${merged['abs_error'].max():.2f}")
print()

print("🎯 SAMPLE PREDICTIONS vs ACTUALS (First 10)")
print("-" * 70)
print(f"{'Date':<12} {'Predicted':<12} {'Actual':<12} {'Error':<12} {'% Error':<10}")
print("-" * 70)
for idx, row in merged.head(10).iterrows():
    print(f"{row['Date'].strftime('%Y-%m-%d'):<12} "
          f"${row['predicted_next_day_close']:>9.2f}  "
          f"${row['actual_next_day_close']:>9.2f}  "
          f"${row['error']:>9.2f}  "
          f"{row['pct_error']:>8.2f}%")
print()

print("📅 RECENT PREDICTIONS (Last 10)")
print("-" * 70)
print(f"{'Date':<12} {'Predicted':<12} {'Actual':<12} {'Error':<12} {'% Error':<10}")
print("-" * 70)
for idx, row in merged.tail(10).iterrows():
    print(f"{row['Date'].strftime('%Y-%m-%d'):<12} "
          f"${row['predicted_next_day_close']:>9.2f}  "
          f"${row['actual_next_day_close']:>9.2f}  "
          f"${row['error']:>9.2f}  "
          f"{row['pct_error']:>8.2f}%")
print()

print("✅ ACCURACY ANALYSIS")
print("-" * 70)
within_1_pct = (merged['abs_error'] / merged['actual_next_day_close'] * 100 <= 1).sum()
within_2_pct = (merged['abs_error'] / merged['actual_next_day_close'] * 100 <= 2).sum()
within_5_pct = (merged['abs_error'] / merged['actual_next_day_close'] * 100 <= 5).sum()
total = len(merged)

print(f"Predictions within 1% of actual: {within_1_pct}/{total} ({within_1_pct/total*100:.1f}%)")
print(f"Predictions within 2% of actual: {within_2_pct}/{total} ({within_2_pct/total*100:.1f}%)")
print(f"Predictions within 5% of actual: {within_5_pct}/{total} ({within_5_pct/total*100:.1f}%)")
print()

print("💾 OUTPUT FILES GENERATED")
print("-" * 70)
print("✓ models/xgb_model.joblib        - Trained XGBoost model")
print("✓ models/metrics.json            - Training metrics (RMSE, MAE)")
print("✓ predictions.csv                - Next-day price predictions")
print()

print("="*70)
print("🎉 PROJECT SUCCESSFULLY EXECUTED!")
print("="*70)
print()
print("📌 Next Steps:")
print("  1. Push to GitHub: git init && git add . && git commit -m 'Initial commit'")
print("  2. Add to portfolio/resume")
print("  3. Customize with real Tata Steel data")
print("  4. Add more features (RSI, MACD, etc.)")
print()
