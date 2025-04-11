import pandas as pd

print("Forensic Log Analyzer")
logs = pd.read_csv("sim_logs.csv")  # Simulated
suspicious = logs[logs['sim_changed'] == True]
print("Suspicious SIM Activity Detected:")
print(suspicious[['user_id', 'timestamp', 'location']])
