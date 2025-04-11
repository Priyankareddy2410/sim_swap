import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Seed for reproducibility
np.random.seed(42)

# Simulate daily transaction totals (in ₹)
days = 40
normal_days = np.random.normal(loc=600, scale=100, size=30)  # Normal behavior
fraud_days = np.random.normal(loc=2200, scale=300, size=10)   # Fraudulent spikes

amounts = np.concatenate([normal_days, fraud_days])
df = pd.DataFrame({'day': range(1, days + 1), 'amount': amounts})

# Detect anomalies
model = IsolationForest(contamination=0.15, random_state=42)
df['anomaly'] = model.fit_predict(df[['amount']])
df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})

# Plotting the bar chart
plt.figure(figsize=(14, 6))
colors = ['red' if a == 1 else 'skyblue' for a in df['anomaly']]
plt.bar(df['day'], df['amount'], color=colors, edgecolor='black')

plt.title("Daily Transaction Totals with Anomalies Detected", fontsize=14)
plt.xlabel("Day", fontsize=12)
plt.ylabel("Total Amount (₹)", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
