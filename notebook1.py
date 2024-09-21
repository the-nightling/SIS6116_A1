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
from matplotlib.animation import PillowWriter

x_values = [i[0] for i in tsp.nodeCoords]
y_values = [i[1] for i in tsp.nodeCoords]

figure1 = plt.figure()  # type: ignore
plt.scatter(x_values, y_values)  # type: ignore
plottedLines = plt.plot([], [], "r-", zorder=0)  # type: ignore

# for i in range(tsp.dimension):
#     plt.annotate(str(i + 1), (x_values[i], y_values[i]))  # type: ignore

plottedLines[0].set_data(x_values, y_values)

# plt.show()  # type: ignore

animationWriter = PillowWriter(fps=15)  # type: ignore

with animationWriter.saving(figure1, "figure1.gif", 100):  # type: ignore
    for i in np.linspace(0, 100):
        plottedLines[0].set_linewidth(i / 10)

        animationWriter.grab_frame()  # type: ignore


## 3. Experiment
import math

totalDistance = 0

for i in range(1, tsp.dimension):
    x1 = x_values[i - 1]
    y1 = y_values[i - 1]
    x2 = x_values[i]
    y2 = y_values[i]
    distance: float = math.dist([x1, y1], [x2, y2])  # type: ignore
    print(f"({x1}, {y1}), ({x2}, {y2}) -> {distance}")
    totalDistance = totalDistance + float(distance)  # type: ignore

print(totalDistance)
