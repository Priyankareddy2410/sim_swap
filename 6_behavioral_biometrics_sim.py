keystroke_times = [0.15, 0.14, 0.13, 0.11, 1.4]  # Simulated

if max(keystroke_times) > 1:
    print(" Anomaly detected in keystroke timing - potential attacker.")
else:
    print(" Typing pattern normal.")
