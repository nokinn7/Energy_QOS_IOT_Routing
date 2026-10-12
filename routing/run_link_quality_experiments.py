
import csv
from pathlib import Path
import routing_algo as algo

OUTPUT_FILE = Path(__file__).with_name(
    "link_quality_results.csv"
)

ALGORITHMS = [
    ("Minimum-hop", algo.minimum_hop_cost),
    ("Energy-aware", algo.energy_aware_cost),
    ("Proposed E-QoS", algo.eqos_cost),
]

def print_eqos_candidate_costs():
    candidates = [
        ["S", "A", "C", "G"],
        ["S", "A", "D", "G"],
        ["S", "B", "D", "G"],
    ]

    print("  E-QoS candidate route costs:")

    for route in candidates:
        total = 0.0

        for u, v in zip(route, route[1:]):
            total += algo.eqos_cost(
                u, v, algo.NETWORK[u][v]
            )

        print(f"    {' -> '.join(route)}: {total:.4f}")


def run_scenario(scenario_name, changed_link, property_name, values):
    original_value = algo.NETWORK[changed_link[0]][changed_link[1]][
        property_name
    ]

    results = []

    try:
        for value in values:
            u, v = changed_link

            # Update the link in both directions
            algo.NETWORK[u][v][property_name] = value
            algo.NETWORK[v][u][property_name] = value

            print(
    f"DEBUG: {u}-{v}, {property_name}={value}, "
    f"forward={algo.NETWORK[u][v][property_name]}, "
    f"reverse={algo.NETWORK[v][u][property_name]}"
)
            print_eqos_candidate_costs()

            for name, cost_function in ALGORITHMS:
                route, cost = algo.find_route("S", "G", cost_function)

                if route is None:
                    continue

                metrics = algo.evaluate_route(route)

                results.append({
                    "scenario": scenario_name,
                    "link": f"{u}-{v}",
                    "tested_value": value,
                    "algorithm": name,
                    "route": " -> ".join(route),
                    "routing_cost": round(cost, 4),
                    "energy_j": metrics["energy"],
                    "delay_ms": metrics["delay"],
                    "estimated_pdr_pct": round(metrics["pdr"], 2),
                    "average_congestion": round(
                        metrics["congestion"], 3
                    ),
                })

                print(
                    f"{scenario_name}={value:.2f} | "
                    f"{name:<14} | {' -> '.join(route)}"
                )

    finally:
        # Restore the original link property
        u, v = changed_link
        algo.NETWORK[u][v][property_name] = original_value
        algo.NETWORK[v][u][property_name] = original_value

    return results


def main():
    
    all_results = []

    # Test reliability of S-B
    all_results.extend(
        run_scenario(
            "reliability",
            ("S", "B"),
            "reliability",
            [0.60, 0.80, 0.98],
        )
    )

    # Test congestion on S-B
    all_results.extend(
        run_scenario(
            "congestion",
            ("S", "B"),
            "congestion",
            [0.10, 0.50, 0.90],
        )
    )

    all_results.extend(
    run_scenario(
        "reliability",
        ("A", "D"),
        "reliability",
        [0.40, 0.60, 0.95],
    )
)

    all_results.extend(
    run_scenario(
        "congestion",
        ("A", "D"),
        "congestion",
        [0.10, 0.50, 0.90],
    )
)

    columns = [
        "scenario", "link", "tested_value", "algorithm",
        "route", "routing_cost", "energy_j", "delay_ms",
        "estimated_pdr_pct", "average_congestion",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nSaved {len(all_results)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
