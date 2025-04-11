import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from scipy.stats import zscore

st.set_page_config(page_title="Advanced SIM-Swap Forensics", layout="wide")

# ---------------------
# 1. Simulated Dataset
# ---------------------
np.random.seed(42)
n1, n2, n3 = 50, 40, 30

phase1 = np.random.normal(loc=550, scale=50, size=n1)
phase2 = np.random.normal(loc=650, scale=90, size=n2)
spikes = np.random.choice([0, 1], size=n2, p=[0.6, 0.4])
phase2 = np.where(spikes == 1, np.random.normal(2500, 400, size=n2), phase2)
phase3 = np.random.normal(loc=6900, scale=500, size=n3)

amounts = np.concatenate([phase1, phase2, phase3])
time_gap = np.abs(np.random.normal(loc=10, scale=4, size=n1 + n2 + n3))
location_jump = np.random.normal(loc=3, scale=1.2, size=n1 + n2 + n3)

df = pd.DataFrame({
    'Index': np.arange(len(amounts)),
    'Amount': amounts,
    'TimeGap': time_gap,
    'LocationChange': location_jump
})

# ---------------------
# 2. Z-score Calculation for Each Feature
# ---------------------
df['Zscore_Amount'] = np.abs(zscore(df['Amount']))
df['Zscore_TimeGap'] = np.abs(zscore(df['TimeGap']))
df['Zscore_Location'] = np.abs(zscore(df['LocationChange']))

# Weighted Z-Anomaly Score
df['Z_Anomaly'] = (
    0.5 * df['Zscore_Amount'] +
    0.3 * df['Zscore_TimeGap'] +
    0.2 * df['Zscore_Location']
)

# ---------------------
# 3. Isolation Forest
# ---------------------
features = df[['Amount', 'TimeGap', 'LocationChange']]
iso_model = IsolationForest(n_estimators=100, contamination=0.3, random_state=42)
df['IsoAnomaly'] = iso_model.fit_predict(features)
df['IsoAnomaly'] = df['IsoAnomaly'].map({1: 0, -1: 1})

# Final Ensemble Logic
df['Anomaly'] = np.where((df['IsoAnomaly'] == 1) | (df['Z_Anomaly'] > 2.0), 1, 0)

# ---------------------
# 4. Sidebar Filters
# ---------------------
st.sidebar.header("Filters")
min_amt = st.sidebar.slider("Minimum Amount (₹)", 0, int(df['Amount'].max()), 500)
max_amt = st.sidebar.slider("Maximum Amount (₹)", 500, int(df['Amount'].max()), 10000)
only_anomalies = st.sidebar.checkbox("Show Only Anomalies", False)

# Filter data
filtered = df[(df['Amount'] >= min_amt) & (df['Amount'] <= max_amt)]
if only_anomalies:
    filtered = filtered[filtered['Anomaly'] == 1]

# ---------------------
# 5. Metrics
# ---------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(df))
col2.metric("Anomalies Detected", df['Anomaly'].sum())
col3.metric("Detection Rate", f"{(df['Anomaly'].sum()/len(df))*100:.1f} %")

# ---------------------
# 6. Line Graph: Amounts
# ---------------------
st.subheader("Transaction Flow")
fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(df["Amount"], label='Amount', color='blue', linewidth=2)
ax1.scatter(df[df["Anomaly"] == 1]["Index"],
            df[df["Anomaly"] == 1]["Amount"],
            color='red', label='Anomaly', marker='x', s=70)
ax1.set_title("Transaction Amounts with Detected Anomalies")
ax1.set_xlabel("Transaction Index")
ax1.set_ylabel("Transaction Amount (₹)")
ax1.legend()
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

# ---------------------
# 7. Z_Anomaly Score Line
# ---------------------
st.subheader("Z-Anomaly Score (Combined Z-Score)")
fig2, ax2 = plt.subplots(figsize=(12, 3))
ax2.plot(df['Z_Anomaly'], color='purple', label='Z-Anomaly Score')
ax2.axhline(2.0, color='red', linestyle='--', label='Anomaly Threshold')
ax2.set_title("Combined Z-Score Anomaly Detection")
ax2.set_xlabel("Transaction Index")
ax2.set_ylabel("Z-Anomaly Score")
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.legend()
st.pyplot(fig2)

# ---------------------
# 8. Data Table
# ---------------------
st.subheader("Transaction Table")
st.dataframe(filtered[['Index', 'Amount', 'TimeGap', 'LocationChange',
                       'Zscore_Amount', 'Zscore_TimeGap', 'Zscore_Location',
                       'Z_Anomaly', 'IsoAnomaly', 'Anomaly']],
             use_container_width=True)

# ---------------------
# 9. Download Section
# ---------------------
st.subheader("Download Detected Anomalies")
csv = df[df['Anomaly'] == 1].to_csv(index=False).encode('utf-8')
st.download_button("Download Anomalies as CSV",
                   csv, "detected_anomalies.csv", mime="text/csv")
