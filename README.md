# Energy and QoS-Aware Intelligent Routing for IoT Networks

## 1. Project Overview

**Project type:** Research and experimental networking prototype  
**Domain:** Internet of Things (IoT), Wireless Sensor Networks (WSNs), routing optimization  
**Team size:** 3 members  
**Development timeline:** 10–14 days  
**Proposed technologies:** NS-3, Python, C/C++, Git and GitHub

### Objective

To design, implement, and experimentally evaluate an intelligent routing approach for IoT networks that considers energy consumption and Quality of Service (QoS).

The proposed approach will be compared against conventional minimum-hop routing and an energy-aware routing baseline under controlled network conditions.

The objective is to determine whether combining energy and QoS metrics can improve network performance without compromising packet delivery reliability.

## 2. Problem Statement

IoT sensors often operate with limited battery energy and communicate over wireless links that may experience congestion, delay, and packet loss.

A routing strategy that prioritizes only hop count or transmission energy may fail to account for these competing requirements.

This project investigates a routing strategy that considers:

- Transmission energy cost.
- Remaining battery energy of intermediate nodes.
- End-to-end packet delay.
- Link reliability and packet-loss risk.
- Network congestion.

The algorithm should select suitable routes while balancing these factors.

## 3. Proposed Solution

The project will begin with a Python routing prototype and progress toward integration with a network simulator.

The proposed implementation will include:

1. A minimum-hop routing baseline.
2. An energy-aware routing baseline.
3. A proposed Energy and QoS-Aware (E-QoS) routing algorithm.
4. Controlled experiments involving network size, traffic load, battery levels, and link quality.
5. Performance analysis using numerical metrics, tables, and graphs.

The initial routing prototype uses a weighted cost function. A learning-based approach, such as Q-learning, may be investigated if time and project requirements permit.

The final implementation method will be documented explicitly.

## 4. Research Questions

1. Can energy-aware routing reduce energy consumption compared with minimum-hop routing?
2. Can the proposed E-QoS algorithm improve the trade-off between energy consumption and QoS?
3. How does routing performance change as traffic load and network size increase?
4. How robust is the routing algorithm when battery levels decrease or wireless links become unreliable?

## 5. Proposed Routing Model

For an eligible link from node i to neighboring node j, the initial proposed cost is:

C(i,j) = wE E(i,j) + wB B(j) + wD D(i,j) + wL L(i,j) + wQ Q(i,j)

Where:

- E(i,j): normalized transmission energy cost.
- B(j): normalized low-battery penalty for the next-hop node.
- D(i,j): normalized link-delay cost.
- L(i,j): link unreliability penalty.
- Q(i,j): normalized congestion penalty.
- wE, wB, wD, wL, wQ: non-negative weights.

The next hop should be selected using a defined route-selection policy, subject to connectivity and loop-prevention constraints.

The metrics must be normalized consistently. The weights will be documented and evaluated experimentally rather than assumed to be optimal.

## 6. Performance Metrics

The following metrics will be evaluated:

- **Energy consumption:** energy used for packet transmission and, where modeled, reception and other relevant operations.
- **Packet Delivery Ratio (PDR):** successfully received packets divided by transmitted packets, expressed as a percentage.
- **End-to-end delay:** average time taken by successfully delivered packets to reach the destination.
- **Throughput:** successfully delivered data per unit of time.
- **Network lifetime:** time until a clearly defined network failure or node-depletion criterion is reached.
- **Routing overhead:** control traffic or other resources required to maintain and select routes.

Additional route-level estimates may be used during the initial prototype but must be distinguished from measurements collected through packet-level simulation.

## 7. Experimental Plan

The algorithms will be evaluated under identical conditions.

Planned scenarios include:

- Different network sizes.
- Low, medium, and high traffic loads.
- Different initial battery levels and battery-depletion conditions.
- Reliable and unreliable wireless links.
- Multiple simulation runs with recorded random seeds.

Results will be reported using comparison tables, graphs, averages, and variability where appropriate.

No performance improvement will be claimed before experimental results support it.

## 8. Technology Stack

- **NS-3:** proposed packet-level network simulator.
- **C/C++:** simulation development and routing integration where required.
- **Python:** routing prototype, result processing, and visualization.
- **NumPy and pandas:** numerical and tabular data analysis.
- **Matplotlib:** experimental plots.
- **Git and GitHub:** version control, collaboration, and code review.

The team will confirm the final simulation approach before implementation. A Python-only prototype must not be presented as an NS-3 simulation.

## 9. Team Responsibilities

### Khushi — Routing Algorithm Lead

- Implement and test the routing cost functions.
- Develop minimum-hop, energy-aware, and proposed E-QoS routing.
- Define route-selection behavior and prevent forwarding loops.
- Validate metric calculations and algorithm behavior.
- Coordinate integration with the simulation lead.

### Saranya — Network Simulation Lead

- Set up and validate the selected simulation environment.
- Model wireless nodes, links, traffic, and packet transmission.
- Integrate the routing implementation with the simulator.
- Export reproducible simulation traces and configuration details.

### Kiruthish — Experiments and Analysis Lead

- Organize experimental scenarios and run records.
- Process simulation outputs and calculate performance metrics.
- Generate comparison graphs and result tables.
- Coordinate the literature review, documentation, and presentation.

All members should understand the overall design and participate in integration and final testing.

## 10. Repository Structure
- `routing/`: proposed routing algorithm and routing utilities.
- `simulation/`: network simulation and trace collection.
- `baselines/`: baseline routing implementations.
- `experiments/`: experiment configurations and execution scripts.
- `analysis/`: metric calculations, comparisons, and plots.
- `results/raw/`: raw experimental outputs.
- `results/processed/`: cleaned and summarized data.
- `results/figures/`: generated plots.
- `tests/`: routing and metric correctness tests.
- `docs/`: methodology, research notes, and final report.
Only files that have actually been implemented should be treated as completed deliverables.

## 11. Development Timeline
### Days 1–3: Foundation
- Set up the repository and development environments.
- Build a working network example.
- Implement and test initial routing methods.
- Establish the output format and evaluation metrics.
### Days 4–7: Integration
- Complete the baseline and proposed routing logic.
- Integrate routing with the selected simulator.
- Produce the first end-to-end experiment.
### Days 8–10: Evaluation
- Run controlled scenarios and repeated trials.
- Compare performance across algorithms.
- Identify and fix correctness or integration problems.
### Days 11–14: Finalization
- Validate results and prepare plots.
- Complete the report and presentation.
- Rehearse the demonstration and prepare backup outputs.
If the deadline is 10 days, the team will prioritize a reproducible working demonstration and complete documentation in parallel.

## 12. Git Collaboration Guidelines
- `main`: stable, reviewed, integrated code.
- `Khushi`: routing algorithm development.
- `Kiruthish`: simulation development.
- `Saranya`: experiment analysis and documentation.
Each member should develop on their assigned branch, commit small logical changes, and push their work regularly.
Use pull requests to merge tested changes into `main`. Communicate before modifying shared interfaces or merging changes that affect other members' work.
Do not commit passwords, access tokens, private credentials, or unnecessary generated files.

## 13. Research Integrity
- Keep algorithm configurations and experimental seeds reproducible.
- Record unsuccessful as well as successful experiments.
- Distinguish simulated measurements from analytical estimates.
- Do not invent results or claim improvements without evidence.
- Document limitations, assumptions, and trade-offs.
- Cite the original research used to motivate the method and baselines.

## 14. Current Project Status
The team has created the GitHub repository and separate development branches. An initial Python routing prototype has been developed.
The next milestones are to validate the routing decisions, complete the E-QoS metric calculations, establish a working network simulation, and conduct controlled comparative experiments.
