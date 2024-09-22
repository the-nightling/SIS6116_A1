## 1. Parse TSP file

import os
from modules.tsp_file_parser import TSP

# problemName = "ulysses16.tsp"
problemName = "a280.tsp"
currentFolderPath = os.path.abspath("")
tspFilePath = os.path.join(currentFolderPath, f"data\\{problemName}")
print("Loading .tsp file from path: " + tspFilePath)

tsp = TSP(tspFilePath)
print(tsp.name + " was loaded")


## 2. Plot TSP Graph

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

x_values: list[float] = [i[0] for i in tsp.nodeCoords]
y_values: list[float] = [i[1] for i in tsp.nodeCoords]

figure1, axis = plt.subplots()  # type: ignore
axis.scatter(x_values, y_values)  # type: ignore
plottedLines = axis.plot([], [], "r-", zorder=0)  # type: ignore

plottedLines[0].set_data(x_values, y_values)
t = np.linspace(0, 100, 100)


def update_data(frame):  # type: ignore
    plottedLines[0].set_linewidth(frame / 10)
    return plottedLines[0]


funcAnimation = FuncAnimation(fig=figure1, func=update_data, frames=len(t), interval=25)  # type: ignore

plt.show()  # type: ignore


## 3. Experiment with computing total distance of initial tour
import math
from aco.node import Node
from aco.utilities import calculate_euclidian_distance

totalDistance = 0

for i in range(1, tsp.dimension):
    x1: float = x_values[i - 1]
    y1: float = y_values[i - 1]
    x2: float = x_values[i]
    y2: float = y_values[i]
    distance: float = math.dist([x1, y1], [x2, y2])  # type: ignore
    distance2: float = calculate_euclidian_distance(Node(x1, y1), Node(x2, y2))

    print(f"({x1}, {y1}), ({x2}, {y2}) -> {distance}")
    totalDistance += distance  # type: ignore

print(totalDistance)
