
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

FOLDER = Path(__file__).parent
CSV_FILE = FOLDER / "experiment_results.csv"
OUTPUT_FOLDER = FOLDER / "plots"
OUTPUT_FOLDER.mkdir(exist_ok=True)

df = pd.read_csv(CSV_FILE)

plots = [
    ("energy_per_packet_j", "Energy per Packet (J)",
     "energy_comparison.png"),
    ("delay_ms", "End-to-End Link Delay (ms)",
     "delay_comparison.png"),
    ("estimated_pdr_pct", "Estimated Packet Delivery Ratio (%)",
     "pdr_comparison.png"),
    ("lowest_relay_battery_pct", "Lowest Relay Battery (%)",
     "battery_comparison.png"),
]

for metric, ylabel, filename in plots:
    plt.figure(figsize=(8, 5))

    for algorithm, group in df.groupby("algorithm"):
        group = group.sort_values("battery_B_j")
        plt.plot(
            group["battery_B_j"],
            group[metric],
            marker="o",
            label=algorithm,
        )

    plt.xlabel("Remaining Battery of Node B (J)")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} vs Node B Battery")
    plt.xticks(sorted(df["battery_B_j"].unique()))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_FOLDER / filename, dpi=200)
    plt.close()

print("Graphs saved to:", OUTPUT_FOLDER)
for _, _, filename in plots:
    print("-", filename)
