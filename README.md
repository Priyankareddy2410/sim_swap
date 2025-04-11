# SIM Swap Fraud Detection System 🔐

This project detects and investigates SIM Swap-based financial fraud using **unsupervised machine learning** and **statistical anomaly detection**. It simulates realistic banking transactions and presents insights using an interactive **Streamlit dashboard**.

---

## 📌 Features

- ✅ **Synthetic Data Simulation**  
  Simulates transactions with realistic user behavior, location changes, and fraud bursts.

- ✅ **Hybrid Fraud Detection**  
  - Isolation Forest (Unsupervised ML)  
  - Z-Score Based Anomaly Scoring  
  - Combined Ensemble Logic for high accuracy

- ✅ **Real-time Dashboard**  
  - Line Graph for transactions  
  - Z-Anomaly Score plot  
  - Interactive filters & table  
  - Export fraud report as CSV

---

## 🧠 How It Works

1. **Data Generation**  
   Simulates 3 phases: normal behavior, random noise, and fraud bursts.

2. **Feature Engineering**  
   - Calculates Z-score for amount, time gaps, and location jumps.  
   - Computes a weighted `Z_Anomaly` score.

3. **Detection Logic**  
   - If **Isolation Forest** OR `Z_Anomaly > 2.0` → transaction flagged.

4. **Visualization**  
   - Everything is rendered in a real-time Streamlit dashboard.

---

## 🛠️ Tech Stack

| Component        | Technology Used      |
|------------------|----------------------|
| Language         | Python 3.10+         |
| ML Model         | Isolation Forest     |
| Statistics       | Scipy Z-score        |
| Web Framework    | Streamlit            |
| Visualization    | Matplotlib           |
| Data Processing  | Pandas, NumPy        |

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/priyankareddy2410/sim_swap.git
cd sim_swap
