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

    def select_next_vertex_AS(self) -> int:
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
            numerator: float = a * b
            denominator += numerator

        random_value: float = random.uniform(0, 1)
        roulette_wheel_position: float = 0.0

        # if pheromone dried up on all unvisited edges, pick random next node
        if denominator == 0:
            print("All neighbouring edges dried up")
            return random.choice(unvisited_vertices)

        for j in unvisited_vertices:
            neighbouring_edge: Edge = self.edges[last_vertex][j]

            a: float = math.pow(neighbouring_edge.pheromone_level, self.alpha)
            b: float = math.pow(1 / neighbouring_edge.cost, self.beta)

            roulette_wheel_position += (a * b) / denominator
            if roulette_wheel_position >= random_value:
                return j

        raise RuntimeError("Could not select next node for ant.")

    def select_next_vertex_ACS(self, q_0: float) -> int:
        unvisited_vertices: list[int] = [
            vertex
            for vertex in range(self.number_of_vertices)
            if vertex not in self.tour
        ]
        last_vertex: int = self.tour[-1]

        max_numerator = 0
        max_numerator_vertex: int = unvisited_vertices[0]
        denominator = 0
        for u in unvisited_vertices:
            neighbouring_edge: Edge = self.edges[last_vertex][u]

            # a280.tsp contains nodes laid on top of each other; then select the unvisited node automatically
            if neighbouring_edge.cost == 0:
                return u

            a: float = math.pow(neighbouring_edge.pheromone_level, self.alpha)
            b: float = math.pow(1 / neighbouring_edge.cost, self.beta)
            numerator: float = a * b

            if numerator > max_numerator:
                max_numerator: float = numerator
                max_numerator_vertex = u

            denominator += numerator

        random_q: float = random.uniform(0, 1)
        if random_q <= q_0:
            return max_numerator_vertex

        random_value: float = random.uniform(0, 1)
        roulette_wheel_position: float = 0.0

        # if pheromone dried up on all unvisited edges, pick random next node
        if denominator == 0:
            print("All neighbouring edges dried up")
            return random.choice(unvisited_vertices)

        for j in unvisited_vertices:
            neighbouring_edge: Edge = self.edges[last_vertex][j]

            a: float = math.pow(neighbouring_edge.pheromone_level, self.alpha)
            b: float = math.pow(1 / neighbouring_edge.cost, self.beta)

            roulette_wheel_position += (a * b) / denominator
            if roulette_wheel_position >= random_value:
                return j

        raise RuntimeError("Could not select next node for ant.")

    def compute_tour_AS(self, start_vertex: int) -> list[int]:
        self.tour = [start_vertex]  # initialise tour with starting node

        while len(self.tour) < self.number_of_vertices:
            self.tour.append(self.select_next_vertex_AS())

        return self.tour

    def compute_tour_ACS(self, start_vertex: int, q_0: float) -> list[int]:
        self.tour = [start_vertex]  # initialise tour with starting node

        while len(self.tour) < self.number_of_vertices:
            self.tour.append(
                self.select_next_vertex_ACS(q_0),
            )

        return self.tour

    def compute_tour_cost(self) -> float:
        self.tour_cost = 0
        for i in range(self.number_of_vertices):
            self.tour_cost += self.edges[self.tour[i]][
                self.tour[(i + 1) % self.number_of_vertices]
            ].cost

        return self.tour_cost
