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

ALGORITHM: str = "AS"
NUMBER_OF_ANTS: int = 52
ALPHA: float = 1
BETA: float = 3
RHO: float = 0.1
Q: float = 1000
INITIAL_PHEROMONE_LEVEL: float = 1
MAXIMUM_NUMBER_OF_ITERATIONS: int = 1000

nodes: list[Node] = [Node(n[0], n[1]) for n in tsp.nodeCoords]


### Setup results logging
def log_results(
    date_time: str,
    run_number: int,
    problem_name: str,
    ellapsed_time: float,
    ant_colony: AntColony,
) -> None:
    with open(f"results_{ALGORITHM}.txt", "a") as file:
        file.write(f"DATE_TIME:{date_time}\n")
        file.write(f"ALGORITHM:{ALGORITHM}\n")
        file.write(f"PROBLEM: {problem_name}\n")
        file.write(f"RUN_NUMBER: {run_number}\n")
        file.write(f"BEST_COST_FOUND: {ant_colony.best_tour_cost}\n")
        file.write(f"TIME_TAKEN: {ellapsed_time}\n")
        file.write(f"NUMBER_OF_ANTS: {NUMBER_OF_ANTS}\n")
        file.write(f"ALPHA: {ALPHA}\n")
        file.write(f"BETA: {BETA}\n")
        file.write(f"RHO: {RHO}\n")
        file.write(f"Q: {Q}\n")
        file.write(f"INITIAL_PHEROMONE_LEVEL: {INITIAL_PHEROMONE_LEVEL}\n")
        file.write(f"MAXIMUM_NUMBER_OF_ITERATIONS: {MAXIMUM_NUMBER_OF_ITERATIONS}\n")
        file.write(f"BEST_TOUR: {ant_colony.best_tour}\n")
        file.write("\n")


### Compute Shortest Path (non-animated version)
# import time
# import datetime

# number_of_runs: int = 1

# for r in range(number_of_runs):
#     ant_colony = AntColony(
#         number_of_ants=NUMBER_OF_ANTS,
#         alpha=ALPHA,
#         beta=BETA,
#         rho=RHO,
#         q=Q,
#         initial_pheromone_level=INITIAL_PHEROMONE_LEVEL,
#         maximum_number_of_iterations=MAXIMUM_NUMBER_OF_ITERATIONS,
#         nodes=nodes,
#     )

#     start_time: float = time.time()
#     ellapsed_time: float = 0

#     for i in range(MAXIMUM_NUMBER_OF_ITERATIONS):
#         ant_colony.iterate()
#         ellapsed_time: float = time.time() - start_time

#         print(
#             f"Iteration {i + 1}; Total cost = {int(ant_colony.best_tour_cost)}; Time ellapsed = {ellapsed_time:.1f}s"
#         )

#     print(f"Best tour found: {ant_colony.best_tour}")
#     print(f"Best cost found: {ant_colony.best_tour_cost}")

#     # for i in range(len(nodes)):
#     #     for j in range(len(nodes)):
#     #         print(f"{int(ant_colony.edges[i][j].pheromone_level)} ", end="")
#     #     print()

#     # log_results(
#     #     date_time=str(datetime.datetime.now()),
#     #     run_number=r,
#     #     problem_name=problem_name,
#     #     ellapsed_time=ellapsed_time,
#     #     ant_colony=ant_colony,
#     # )


### Compute Shortest Path (animated output)
import matplotlib.pyplot as plt
import networkx as nx
import time
from matplotlib.animation import FuncAnimation

x_values: list[float] = [i[0] for i in tsp.nodeCoords]
y_values: list[float] = [i[1] for i in tsp.nodeCoords]

# Plot TSP Graph
G = nx.complete_graph(len(nodes))  # type: ignore
node_positions: dict[int, tuple[float, float]] = {
    i: (x_values[i], y_values[i]) for i in range(len(nodes))
}

figure1, axis = plt.subplots()  # type: ignore
nx.draw_networkx_nodes(G, node_positions, ax=axis, node_size=10)  # type: ignore

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


EDGE_TRANSPARENCY_SCALING_FACTOR: int = 30


# One iteration of the animation
def update_data(frame):  # type: ignore
    ant_colony.iterate()

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
    axis.set_title(
        f"Iteration {frame + 1}\nTotal cost = {int(ant_colony.best_tour_cost)}\nTime ellapsed = {ellapsed_time:.1f}s"
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
ani = FuncAnimation(
    figure1,
    update_data,  # type: ignore
    frames=MAXIMUM_NUMBER_OF_ITERATIONS,
    interval=100,
    blit=False,
    repeat=False,
)

start_time: float = time.time()
plt.show()  # type: ignore


# a280.tsp
# best so far is cost of 3050 with
# NUMBER_OF_ANTS: int = 30
# ALPHA: float = 1
# BETA: float = 3
# RHO: float = 0.1
# INITIAL_PHEROMONE_LEVEL: float = 1
# MAXIMUM_NUMBER_OF_ITERATIONS: int = 300

# berlin52.tsp
# best so far is cost of 7544 with
# NUMBER_OF_ANTS: int = 104
# ALPHA: float = 1
# BETA: float = 3
# RHO: float = 0.1
# INITIAL_PHEROMONE_LEVEL: float = 1
# MAXIMUM_NUMBER_OF_ITERATIONS: int = 1000

# TODO
# * log time taken
# * log results to file
# - log last best iteration
# * fix last path of tour not plotted in animation
# - improve algorithm to use ACS instead of AS
# - add stopping criteria other than number of iterations
# - plot known optimal path if available
# * stretch goal: plot animated pheromone trails
