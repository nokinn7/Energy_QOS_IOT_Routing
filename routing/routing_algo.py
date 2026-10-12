
import heapq
from math import prod

# Remaining and initial battery energy, in joules
INITIAL_ENERGY = {n: 100.0 for n in "SABCDG"}

ENERGY = {
    "S": 100.0, "A": 90.0, "B": 5.0,
    "C": 80.0, "D": 75.0, "G": 100.0
}

# Undirected links with illustrative properties:
# (node1, node2, energy per packet, delay in ms,
#  reliability, congestion)
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

    return 0.7 * link["energy"] + 0.3 * battery_penalty



def eqos_cost(u, v, link):
    battery_ratio = ENERGY[v] / INITIAL_ENERGY[v]

    energy_cost = link["energy"] / 1.0
    battery_penalty = 1.0 - battery_ratio
    delay_cost = link["delay"] / 8.0
    loss_cost = 1.0 - link["reliability"]
    congestion_cost = link["congestion"]

    return (
        0.20 * energy_cost
        + 0.50 * battery_penalty
        + 0.15 * delay_cost
        + 0.10 * loss_cost
        + 0.05 * congestion_cost
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


def evaluate_route(route):
    if not route or len(route) < 2:
        return None

    links = [
        NETWORK[u][v]
        for u, v in zip(route, route[1:])
    ]

    total_energy = sum(link["energy"] for link in links)
    total_delay = sum(link["delay"] for link in links)

    delivery_probability = prod(
        link["reliability"] for link in links
    )

    average_congestion = sum(
        link["congestion"] for link in links
    ) / len(links)

    intermediate_nodes = route[1:-1]

    bottleneck_battery = min(
        (
            100.0 * ENERGY[node] / INITIAL_ENERGY[node]
            for node in intermediate_nodes
        ),
        default=100.0
    )

    return {
        "hops": len(links),
        "energy": total_energy,
        "delay": total_delay,
        "pdr": 100.0 * delivery_probability,
        "congestion": average_congestion,
        "battery": bottleneck_battery,
    }


def main():
    algorithms = [
        ("Minimum-hop", minimum_hop_cost),
        ("Energy-aware", energy_aware_cost),
        ("Proposed E-QoS", eqos_cost),
    ]

    print("ENERGY AND QoS-AWARE ROUTING")
    print("=" * 55)

    for name, cost_function in algorithms:
        route, cost = find_route("S", "G", cost_function)

        print(f"\n{name}")

        if route is None:
            print("No route found.")
            continue

        metrics = evaluate_route(route)

        print("Route:", " -> ".join(route))
        print(f"Routing cost: {cost:.4f}")
        print(f"Hop count: {metrics['hops']}")
        print(f"Energy per packet: {metrics['energy']:.2f} J")
        print(f"End-to-end link delay: {metrics['delay']:.2f} ms")
        print(f"Estimated PDR: {metrics['pdr']:.2f}%")
        print(f"Average congestion: {metrics['congestion']:.2f}")
        print(
            "Lowest intermediate-node battery: "
            f"{metrics['battery']:.1f}%"
        )


if __name__ == "__main__":
    main()
