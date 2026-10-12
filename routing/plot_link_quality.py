
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).parent
df = pd.read_csv(folder / "link_quality_results.csv")

output = folder / "link_quality_plots"
output.mkdir(exist_ok=True)

metrics = [
    ("estimated_pdr_pct", "Estimated PDR (%)", "pdr"),
    ("delay_ms", "End-to-end delay (ms)", "delay"),
    ("energy_j", "Energy per packet (J)", "energy"),
]

# Reliability experiment: S-B link only
reliability_sb = df[
    (df["scenario"] == "reliability") &
    (df["link"] == "S-B")
]

reliability_ad = df[
    (df["scenario"] == "reliability") &
    (df["link"] == "A-D")
]

# Congestion experiments: plot each link separately
experiments = [
    ("reliability", "S-B", reliability_sb),
("reliability", "A-D", reliability_ad),
]

for scenario, link, subset in experiments:
    for metric, ylabel, suffix in metrics:
        plt.figure(figsize=(8, 5))

        for algorithm, group in subset.groupby("algorithm"):
            group = group.sort_values("tested_value")
            plt.plot(
                group["tested_value"],
                group[metric],
                marker="o",
                label=algorithm,
            )

        x_label = (
            "Link reliability"
            if scenario == "reliability"
            else "Link congestion"
        )

        plt.xlabel(x_label)
        plt.ylabel(ylabel)
        plt.title(f"{ylabel} vs {x_label} on link {link}")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(
            output / f"{scenario}_{link.replace('-', '')}_{suffix}.png",
            dpi=200,
        )
        plt.close()

print("Corrected plots saved to:", output)
