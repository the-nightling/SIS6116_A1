import math
from node import Node


def calculate_euclidian_distance(a: Node, b: Node) -> float:
    return math.sqrt(math.pow(b.x - a.x, 2) + math.pow(b.y - a.y, 2))
