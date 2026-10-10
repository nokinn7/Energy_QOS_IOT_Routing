
import heapq

# Remaining and initial battery energy, in joules
INITIAL_ENERGY = {n: 100.0 for n in "SABCDG"}
ENERGY = {
    "S": 100.0, "A": 90.0, "B": 20.0,
    "C": 80.0, "D": 75.0, "G": 100.0
}

# Undirected links with illustrative properties
RAW_LINKS = [
    ("S", "A", 1.0, 5.0, 0.99, 0.2),
    ("S", "B", 0.5, 2.0, 0.98, 0.1),
    ("A", "C", 1.0, 5.0, 0.99, 0.2),
    ("A", "D", 0.8, 8.0, 0.95, 0.5),
    ("B", "D", 0.5, 2.0, 0.98, 0.1),
    ("C", "G", 1.0, 5.0, 0.99, 0.2),
    ("D", "G", 0.5, 2.0, 0.98, 0.1),
]

NETWORK = {n: {} for n in INITIAL_ENERGY}

for u, v, energy, delay, reliability, congestion in RAW_LINKS:
    link = {
        "energy": energy,
        "delay": delay,
        "reliability": reliability,
        "congestion": congestion,
    }
    NETWORK[u][v] = link
    NETWORK[v][u] = link.copy()


def minimum_hop_cost(u, v, link):
    return 1.0


def energy_aware_cost(u, v, link):
    battery_ratio = ENERGY[v] / INITIAL_ENERGY[v]
    battery_penalty = 1.0 - battery_ratio
    return 0.7 * (link["energy"] / 1.0) + 0.3 * battery_penalty

def eqos_cost(u, v, link):
    battery_ratio = ENERGY[v] / INITIAL_ENERGY[v]

    energy_cost = link["energy"] / 1.0
    battery_penalty = 1.0 - battery_ratio
    delay_cost = link["delay"] / 8.0
    loss_cost = 1.0 - link["reliability"]
    congestion_cost = link["congestion"]

    return (
        0.30 * energy_cost
        + 0.25 * battery_penalty
        + 0.20 * delay_cost
        + 0.15 * loss_cost
        + 0.10 * congestion_cost
    )

def find_route(source, destination, cost_function):
    queue = [(0.0, source)]
    best = {source: 0.0}
    previous = {}

    while queue:
        cost, current = heapq.heappop(queue)

        if cost > best.get(current, float("inf")):
            continue

        if current == destination:
            break

        for neighbor, link in NETWORK[current].items():
            step = cost_function(current, neighbor, link)
            new_cost = cost + step

            if new_cost < best.get(neighbor, float("inf")):
                best[neighbor] = new_cost
                previous[neighbor] = current
                heapq.heappush(queue, (new_cost, neighbor))

    if destination not in best:
        return None, float("inf")

    route = []
    node = destination

    while node != source:
        route.append(node)
        node = previous[node]

    route.append(source)
    route.reverse()

    return route, best[destination]
def main():
    algorithms = [
        ("Minimum-hop", minimum_hop_cost),
        ("Energy-aware", energy_aware_cost),
        ("Proposed E-QoS", eqos_cost),
    ]

    print("ENERGY AND QoS-AWARE ROUTING")
    print("-" * 40)

    for name, cost_function in algorithms:
        route, cost = find_route("S", "G", cost_function)
        print(f"\n{name}")

        if route:
            print("Route:", " -> ".join(route))
            print(f"Routing cost: {cost:.4f}")
        else:
            print("No route found.")


if __name__ == "__main__":
    main()