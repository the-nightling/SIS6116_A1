### Parse TSP file

import os
from modules.tsp_file_parser.tsp_file_parser import TSP

# problemName = "ulysses16.tsp"
# problemName = "a280.tsp"
problem_name = "berlin52.tsp"
currentFolderPath: str = os.path.abspath("")
tspFilePath = os.path.join(currentFolderPath, f"data\\{problem_name}")
print("Loading .tsp file from path: " + tspFilePath)

tsp = TSP(tspFilePath)
print(tsp.name + " was loaded")


### Initialise ACO parameters

from modules.aco.node import Node
from modules.aco.ant_colony import AntColony

ALGORITHM: str = "ACS"
NUMBER_OF_ANTS: int = 52
ALPHA: float = 1
BETA: float = 5
RHO: float = 0.1
Q: float = 1000
Q_0: float = 0.1  # aka r_0
INITIAL_PHEROMONE_LEVEL: float = 10
MAXIMUM_NUMBER_OF_ITERATIONS: int = 1000
LOG_RESULTS: bool = True

nodes: list[Node] = [Node(n[0], n[1]) for n in tsp.nodeCoords]


### Setup results logging
def log_results(
    date_time: str,
    run_number: int,
    problem_name: str,
    ellapsed_time: float,
    ant_colony: AntColony,
    max_pheromone_level_reached: float,
    min_pheromone_level_reached: float,
) -> None:
    with open(f"results/results_{ALGORITHM}.txt", "a") as file:
        file.write(f"DATE_TIME:{date_time}\n")
        file.write(f"ALGORITHM:{ALGORITHM}\n")
        file.write(f"PROBLEM: {problem_name}\n")
        file.write(f"RUN_NUMBER: {run_number}\n")
        file.write(f"BEST_COST_FOUND: {ant_colony.best_tour_cost}\n")
        file.write(f"TIME_TAKEN: {ellapsed_time}\n")
        file.write(
            f"DRY_NEIGBOURING_EDGES_COUNTER: {ant_colony.dry_neighbouring_edges_counter[0]}\n"
        )
        file.write(f"MAX_PHEROMONE_LEVEL_REACHED: {max_pheromone_level_reached}\n")
        file.write(f"MIN_PHEROMONE_LEVEL_REACHED: {min_pheromone_level_reached}\n")
        file.write(f"NUMBER_OF_ANTS: {NUMBER_OF_ANTS}\n")
        file.write(f"ALPHA: {ALPHA}\n")
        file.write(f"BETA: {BETA}\n")
        file.write(f"RHO: {RHO}\n")
        file.write(f"Q: {Q}\n")
        file.write(f"Q_0: {Q_0}\n")
        file.write(f"INITIAL_PHEROMONE_LEVEL: {INITIAL_PHEROMONE_LEVEL}\n")
        file.write(f"MAXIMUM_NUMBER_OF_ITERATIONS: {MAXIMUM_NUMBER_OF_ITERATIONS}\n")
        file.write(f"BEST_TOUR: {ant_colony.best_tour}\n")
        file.write("\n")


def log_run_results(
    date_time: str,
    problem_name: str,
    ellapsed_time: float,
    cost_avg: float,
    cost_std: float,
    dry_neighbouring_edges_counter: int,
):
    with open(f"results/run_results_{ALGORITHM}.txt", "a") as file:
        file.write(f"DATE_TIME:{date_time}\n")
        file.write(f"ALGORITHM:{ALGORITHM}\n")
        file.write(f"PROBLEM: {problem_name}\n")
        file.write(f"COST_AVERAGE: {cost_avg}\n")
        file.write(f"COST_STANDARD_DEVIATION: {cost_std}\n")
        file.write(f"TIME_TAKEN: {ellapsed_time}\n")
        file.write(f"DRY_NEIGBOURING_EDGES_COUNTER: {dry_neighbouring_edges_counter}\n")
        file.write(f"NUMBER_OF_ANTS: {NUMBER_OF_ANTS}\n")
        file.write(f"ALPHA: {ALPHA}\n")
        file.write(f"BETA: {BETA}\n")
        file.write(f"RHO: {RHO}\n")
        file.write(f"Q: {Q}\n")
        file.write(f"Q_0: {Q_0}\n")
        file.write(f"INITIAL_PHEROMONE_LEVEL: {INITIAL_PHEROMONE_LEVEL}\n")
        file.write(f"MAXIMUM_NUMBER_OF_ITERATIONS: {MAXIMUM_NUMBER_OF_ITERATIONS}\n")
        file.write("\n")


### Compute Shortest Path (non-animated version)
import time
import datetime
import numpy as np

number_of_runs: int = 10
run_costs: list[float] = []
ellapsed_times: list[float] = []
dry_neighbouring_edges_counters: list[int] = []

for r in range(number_of_runs):
    # Initialise algorithm with chosen parameters
    ant_colony = AntColony(
        number_of_ants=NUMBER_OF_ANTS,
        alpha=ALPHA,
        beta=BETA,
        rho=RHO,
        q=Q,
        initial_pheromone_level=INITIAL_PHEROMONE_LEVEL,
        maximum_number_of_iterations=MAXIMUM_NUMBER_OF_ITERATIONS,
        nodes=nodes,
    )

    start_time: float = time.time()
    ellapsed_time: float = 0

    # Iterate through algorithm
    for i in range(MAXIMUM_NUMBER_OF_ITERATIONS):
        if ALGORITHM == "AS":  # type: ignore
            ant_colony.iterate_AS()
        elif ALGORITHM == "ACS":
            ant_colony.iterate_ACS(Q_0)

        ellapsed_time: float = time.time() - start_time

        print(
            f"Iteration {i + 1}; Total cost = {int(ant_colony.best_tour_cost)}; Time ellapsed = {ellapsed_time:.1f}s; Dry neighbouring edges counter = {ant_colony.dry_neighbouring_edges_counter[0]}"
        )

    # Output results
    print(f"Best tour found: {ant_colony.best_tour}")
    print(f"Best cost found: {ant_colony.best_tour_cost}")

    run_costs.append(ant_colony.best_tour_cost)
    ellapsed_times.append(ellapsed_time)
    dry_neighbouring_edges_counters.append(ant_colony.dry_neighbouring_edges_counter[0])

    max_pheromone_level = float("-inf")
    min_pheromone_level = float("inf")
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            pheromone_level: float = ant_colony.edges[i][j].pheromone_level
            if max_pheromone_level < pheromone_level:
                max_pheromone_level: float = pheromone_level

            if min_pheromone_level > pheromone_level:
                min_pheromone_level: float = pheromone_level

    print(f"Max pheromone level reached: {max_pheromone_level:.2f}")
    print(f"Min pheromone level reached: {min_pheromone_level:.2f}")

    if LOG_RESULTS:
        log_results(
            date_time=str(datetime.datetime.now()),
            run_number=r,
            problem_name=problem_name,
            ellapsed_time=ellapsed_time,
            ant_colony=ant_colony,
            max_pheromone_level_reached=max_pheromone_level,
            min_pheromone_level_reached=min_pheromone_level,
        )

run_costs_avg = float(np.mean(run_costs))
run_costs_std_dev = float(np.std(run_costs))
ellapsed_time_avg = float(np.mean(ellapsed_times))
dry_neighbouring_edges_counter_avg = int(np.mean(dry_neighbouring_edges_counters))

log_run_results(
    date_time=str(datetime.datetime.now()),
    problem_name=problem_name,
    ellapsed_time=ellapsed_time_avg,
    cost_avg=run_costs_avg,
    cost_std=run_costs_std_dev,
    dry_neighbouring_edges_counter=dry_neighbouring_edges_counter_avg,
)


## Compute Shortest Path (animated output)
import matplotlib.pyplot as plt
import networkx as nx
import time
import datetime
import matplotlib.animation as animation

x_values: list[float] = [i[0] for i in tsp.nodeCoords]
y_values: list[float] = [i[1] for i in tsp.nodeCoords]

# Plot TSP Graph
G = nx.complete_graph(len(nodes))  # type: ignore
node_positions: dict[int, tuple[float, float]] = {
    i: (x_values[i], y_values[i]) for i in range(len(nodes))
}

figure1, axis = plt.subplots()  # type: ignore
nx.draw_networkx_nodes(G, node_positions, ax=axis, node_size=10)  # type: ignore
axis_text = axis.text(
    -50,
    -50,
    f"Iteration 0\nTotal cost = 0\nTime ellapsed = 0.0s\nDry neighbouring edges counter = 0",
)

# Initialize best tour plot for an iteration
tour_line = axis.plot([], [], "r-", zorder=1)[0]

# Initialize edge plots and store them in a dictionary where the key is the node indices like (node_i, node_j)
edges = list(G.edges())  # type: ignore
edge_lines_dict = {  # type: ignore
    (edge[0], edge[1]): axis.plot(
        [node_positions[edge[0]][0], node_positions[edge[1]][0]],
        [node_positions[edge[0]][1], node_positions[edge[1]][1]],
        color="gray",
        alpha=0,
        zorder=0,
    )[0]
    for edge in edges  # type: ignore
}


# Creates tour coordinates for a particular tour so that it can be plotted
def create_tour_coords(tour: list[int]) -> list[tuple[float, float]]:
    coords: list[tuple[float, float]] = []
    for n in tour:
        coords.append((x_values[n], y_values[n]))
    coords.append(coords[0])

    return coords


EDGE_TRANSPARENCY_SCALING_FACTOR: int = 5

start_time: float = time.time()


# One iteration of the animation
def update_data(frame):  # type: ignore
    if ALGORITHM == "AS":
        ant_colony.iterate_AS()
    elif ALGORITHM == "ACS":
        ant_colony.iterate_ACS(Q_0)

    print(frame)
    global start_time
    ellapsed_time: float = time.time() - start_time

    # update transparency of an edge based on the pheromone level
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j:
                continue

            edge_pheromone_level: float = ant_colony.edges[i][j].pheromone_level
            edge_alpha: float = edge_pheromone_level / EDGE_TRANSPARENCY_SCALING_FACTOR
            if edge_alpha > 1:
                edge_alpha = 1

            edge_nodes: tuple[int, int] = (
                (i, j) if (i, j) in edge_lines_dict else (j, i)
            )
            edge_lines_dict[edge_nodes].set_alpha(edge_alpha)

    # update plot of best tour found so far
    tour_coords: list[tuple[float, float]] = create_tour_coords(ant_colony.best_tour)
    x_tour_coords: list[float] = [c[0] for c in tour_coords]
    y_tour_coords: list[float] = [c[1] for c in tour_coords]

    tour_line.set_data(x_tour_coords, y_tour_coords)
    axis_text.set_text(
        f"Iteration {frame + 1}\nTotal cost = {int(ant_colony.best_tour_cost)}\nTime ellapsed = {ellapsed_time:.1f}s\nDry neighbouring edges counter = {ant_colony.dry_neighbouring_edges_counter[0]}",
    )

    return [tour_line, *edge_lines_dict.values()]


# Initialize algorithm with desired parameters
ant_colony = AntColony(
    number_of_ants=NUMBER_OF_ANTS,
    alpha=ALPHA,
    beta=BETA,
    rho=RHO,
    q=Q,
    initial_pheromone_level=INITIAL_PHEROMONE_LEVEL,
    maximum_number_of_iterations=MAXIMUM_NUMBER_OF_ITERATIONS,
    nodes=nodes,
)

# Create the animation
ani = animation.FuncAnimation(
    figure1,
    update_data,  # type: ignore
    frames=MAXIMUM_NUMBER_OF_ITERATIONS,
    interval=100,
    blit=False,
    repeat=False,
)

now: str = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
metadata: dict[str, str] = {
    "ALPHA": str(ALPHA),
    "BETA": str(BETA),
    "RHO": str(RHO),
    "Q": str(Q),
    "Q_0": str(Q_0),
    "INITIAL_PHEROMONE_LEVEL": str(INITIAL_PHEROMONE_LEVEL),
}
writer = animation.PillowWriter(fps=50, metadata=metadata)
ani.save(f"results/{ALGORITHM}_{now}.gif", writer=writer)


# plt.show()  # type: ignore

max_pheromone_level = float("-inf")
min_pheromone_level = float("inf")
for i in range(len(nodes)):
    for j in range(len(nodes)):
        pheromone_level = ant_colony.edges[i][j].pheromone_level
        if max_pheromone_level < pheromone_level:
            max_pheromone_level = pheromone_level

        if min_pheromone_level > pheromone_level:
            min_pheromone_level = pheromone_level

print(f"Max pheromone level reached: {max_pheromone_level:.2f}")
print(f"Min pheromone level reached: {min_pheromone_level:.2f}")
