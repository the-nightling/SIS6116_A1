### Parse TSP file

import os
from modules.tsp_file_parser.tsp_file_parser import TSP

# problemName = "ulysses16.tsp"
problemName = "a280.tsp"
currentFolderPath = os.path.abspath("")
tspFilePath = os.path.join(currentFolderPath, f"data\\{problemName}")
print("Loading .tsp file from path: " + tspFilePath)

tsp = TSP(tspFilePath)
print(tsp.name + " was loaded")


### Plot TSP Graph

import matplotlib.pyplot as plt


x_values: list[float] = [i[0] for i in tsp.nodeCoords]
y_values: list[float] = [i[1] for i in tsp.nodeCoords]

figure1, axis = plt.subplots()  # type: ignore
axis.scatter(x_values, y_values)  # type: ignore
plottedLines = axis.plot([], [], "r-", zorder=0)  # type: ignore


### Initialise ACO (AS) parameters

from modules.aco.node import Node
from modules.aco.ant_colony import AntColony

NUMBER_OF_ANTS: int = 3
ALPHA: float = 1
BETA: float = 3
RHO: float = 0.1
INITIAL_PHEROMONE_LEVEL: float = 1
MAXIMUM_NUMBER_OF_ITERATIONS: int = 1000

nodes: list[Node] = [Node(n[0], n[1]) for n in tsp.nodeCoords]

ant_colony = AntColony(
    NUMBER_OF_ANTS,
    ALPHA,
    BETA,
    RHO,
    INITIAL_PHEROMONE_LEVEL,
    MAXIMUM_NUMBER_OF_ITERATIONS,
    nodes,
)

### Compute shortest path

# for i in range(MAXIMUM_NUMBER_OF_ITERATIONS):
#     if i > MAXIMUM_NUMBER_OF_ITERATIONS:
#         break

#     ant_colony.iterate()
#     print(ant_colony.best_tour_cost)

# print(ant_colony.best_tour)

from matplotlib.animation import FuncAnimation

plottedLines[0].set_data(x_values, y_values)  # type: ignore


def create_tour_coords(tour: list[int]) -> list[tuple[float, float]]:
    coords: list[tuple[float, float]] = []
    for n in tour:
        coords.append((x_values[n], y_values[n]))

    return coords


def update_data(frame):  # type: ignore
    ant_colony.iterate()

    tour_coords: list[tuple[float, float]] = create_tour_coords(ant_colony.best_tour)
    x_tour_coords: list[float] = [c[0] for c in tour_coords]
    y_tour_coords: list[float] = [c[1] for c in tour_coords]

    plottedLines[0].set_data(x_tour_coords, y_tour_coords)
    axis.set_title(
        f"Iteration {frame + 1}\nTotal cost = {int(ant_colony.best_tour_cost)}"
    )

    return plottedLines[0]


funcAnimation = FuncAnimation(fig=figure1, func=update_data, frames=MAXIMUM_NUMBER_OF_ITERATIONS, interval=25, repeat=False)  # type: ignore

plt.show()  # type: ignore

print(f"Best cost found: {ant_colony.best_tour_cost}")
