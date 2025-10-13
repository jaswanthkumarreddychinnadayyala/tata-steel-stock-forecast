import pandas as pd
import numpy as np

# Generate more realistic sample data
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=100, freq='D')
base_price = 100
prices = [base_price]

# Generate more realistic stock prices with trend and noise
for i in range(99):
    change = np.random.normal(0.001, 0.02)  # slight upward bias with volatility
    new_price = prices[-1] * (1 + change)
    prices.append(new_price)

df = pd.DataFrame({
    'Date': dates,
    'Open': [p * (1 + np.random.uniform(-0.01, 0.01)) for p in prices],
    'High': [p * (1 + np.random.uniform(0.005, 0.02)) for p in prices],
    'Low': [p * (1 + np.random.uniform(-0.02, -0.005)) for p in prices],
    'Close': prices,
    'Volume': [int(np.random.uniform(100000, 500000)) for _ in prices]
})

df.to_csv('data/sample_data.csv', index=False)
print(f"Generated {len(df)} rows of sample data")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nLast 5 rows:")
print(df.tail())
print(f"\nPrice range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
