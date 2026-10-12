
import csv
from pathlib import Path
import routing_algo as algo

BATTERY_LEVELS = [5, 20, 50, 80]

ALGORITHMS = [
    ("Minimum-hop", algo.minimum_hop_cost),
    ("Energy-aware", algo.energy_aware_cost),
    ("Proposed E-QoS", algo.eqos_cost),
]

OUTPUT_FILE = Path(__file__).with_name("experiment_results.csv")


def main():
    columns = [
        "battery_B_j",
        "algorithm",
        "route",
        "routing_cost",
        "hop_count",
        "energy_per_packet_j",
        "delay_ms",
        "estimated_pdr_pct",
        "average_congestion",
        "lowest_relay_battery_pct",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for battery in BATTERY_LEVELS:
            # Reset B's remaining battery for this scenario
            algo.ENERGY["B"] = float(battery)

            for name, cost_function in ALGORITHMS:
                route, cost = algo.find_route(
                    "S", "G", cost_function
                )

                if route is None:
                    print(f"No route found for {name}, B={battery} J")
                    continue

                metrics = algo.evaluate_route(route)

                row = {
                    "battery_B_j": battery,
                    "algorithm": name,
                    "route": " -> ".join(route),
                    "routing_cost": round(cost, 4),
                    "hop_count": metrics["hops"],
                    "energy_per_packet_j": metrics["energy"],
                    "delay_ms": metrics["delay"],
                    "estimated_pdr_pct": round(metrics["pdr"], 2),
                    "average_congestion": round(
                        metrics["congestion"], 3
                    ),
                    "lowest_relay_battery_pct": round(
                        metrics["battery"], 1
                    ),
                }

                writer.writerow(row)
                print(
                    f"B={battery:>2} J | {name:<14} | "
                    f"{row['route']:<17} | "
                    f"Energy={row['energy_per_packet_j']:.2f} J | "
                    f"Delay={row['delay_ms']:.1f} ms"
                )

    print(f"\nExperiment complete. Results saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
