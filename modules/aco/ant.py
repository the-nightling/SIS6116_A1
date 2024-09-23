import math
import random


class Edge:
    def __init__(self, a: int, b: int, cost: float, pheromone_level: float) -> None:
        self.a: int = a
        self.b: int = b
        self.cost: float = cost
        self.pheromone_level: float = pheromone_level


class Ant:
    def __init__(
        self,
        edges: list[list[Edge]],
        alpha: float,
        beta: float,
        number_of_vertices: int,
    ) -> None:
        self.edges: list[list[Edge]] = edges
        self.alpha: float = alpha
        self.beta: float = beta
        self.number_of_vertices: int = number_of_vertices
        self.tour: list[int] = []
        self.tour_cost: float = 0.0

    def select_next_vertex(self) -> int:
        unvisited_vertices: list[int] = [
            vertex
            for vertex in range(self.number_of_vertices)
            if vertex not in self.tour
        ]
        last_vertex: int = self.tour[-1]

        denominator = 0
        for u in unvisited_vertices:
            neighbouring_edge: Edge = self.edges[last_vertex][u]

            # a280.tsp contains nodes laid on top of each other; then select the unvisited node automatically
            if neighbouring_edge.cost == 0:
                return u

            a: float = math.pow(neighbouring_edge.pheromone_level, self.alpha)
            b: float = math.pow(1 / neighbouring_edge.cost, self.beta)

            denominator += a * b

        random_value: float = random.uniform(0, 1)
        roulette_wheel_position: float = 0.0

        # if pheromone dried up on all unvisited edges, pick random next node
        if denominator == 0:
            return random.choice(unvisited_vertices)

        for j in unvisited_vertices:
            neighbouring_edge: Edge = self.edges[last_vertex][j]

            a: float = math.pow(neighbouring_edge.pheromone_level, self.alpha)
            b: float = math.pow(1 / neighbouring_edge.cost, self.beta)

            roulette_wheel_position += (a * b) / denominator
            if roulette_wheel_position >= random_value:
                return j

        raise RuntimeError("Could not select next node for ant.")

    def compute_tour(self) -> list[int]:
        self.tour = [
            random.randint(0, self.number_of_vertices - 1)
        ]  # initialise tour with starting node

        while len(self.tour) < self.number_of_vertices:
            self.tour.append(self.select_next_vertex())

        return self.tour

    def compute_tour_cost(self) -> float:
        self.tour_cost = 0
        for i in range(self.number_of_vertices):
            self.tour_cost += self.edges[self.tour[i]][
                self.tour[(i + 1) % self.number_of_vertices]
            ].cost

        return self.tour_cost
