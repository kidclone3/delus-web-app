import math
import random
from typing import List, Tuple, Optional

from config import *
from data.obstacles import obstacles

Obstacle = Tuple[int, int, int, int, Optional[str]]
Obstacles = List[Obstacle]
CoordPair = Tuple[int, int]
Graph = List[List[int]]


def get_obstacles(list_obstacles: Obstacles) -> set[str]:
    obstacles_set = set()

    for each_obstacle in list_obstacles:
        x_start, x_end, y_start, y_end = each_obstacle[:4]
        x = x_start
        while x <= x_end:
            y = y_start
            while y <= y_end:
                obstacles_set.add(f"{x}:{y}")
                y += 1
            x += 1

    return obstacles_set


def get_roads_nodes() -> List[CoordPair]:
    road_nodes = []
    obstacles_set = get_obstacles(obstacles)

    for x in range(GRID_COUNT):
        for y in range(GRID_COUNT):
            if f"{x}:{y}" not in obstacles_set:
                road_nodes.append((x, y))
    return road_nodes


def build_graph(obstacles_set: set, grid_count: int) -> Graph:
    graph = []
    for y in range(grid_count):
        row = []
        for x in range(grid_count):
            if f"{x}:{y}" in obstacles_set:
                row.append(0)
            else:
                row.append(1)
        graph.append(row)
    return graph


cache_graph = None


def get_graph() -> Graph:
    global cache_graph
    if cache_graph is None:
        obstacles_set = get_obstacles(obstacles)
        graph = build_graph(obstacles_set, GRID_COUNT)
        # print(graph)
        cache_graph = graph

    return cache_graph


def get_destination_range(coord: int) -> Tuple[int, int]:
    if coord < GRID_COUNT / 2:
        return GRID_COUNT // 2 + coord // 2, GRID_COUNT
    else:
        return 0, GRID_COUNT // 2 - (GRID_COUNT - coord) // 2


def get_closet_road_node(x: int, y: int, graph: Graph) -> CoordPair:
    def is_valid(y, x):
        return 0 < y < len(graph) - 1 and 0 < x < len(graph[y]) - 1

    if is_valid(y, x) and graph[y][x] == 1:
        return x, y

    directions = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0)
    ]

    queue = [(y, x)]
    seen = {(y, x)}

    while queue:
        y, x = queue.pop(0)

        for dx, dy in directions:
            next_y = y + dy
            next_x = x + dx

            if is_valid(next_y, next_x) and (next_y, next_x) not in seen:
                if graph[next_y][next_x] == 1:
                    return next_x, next_y
                seen.add((next_y, next_x))
                queue.append((next_y, next_x))


def generate_destination(coord_pair: CoordPair) -> CoordPair:
    graph = get_graph()

    start_x, start_y = coord_pair
    range_x = get_destination_range(start_x)
    range_y = get_destination_range(start_y)

    dest_x = random.randint(range_x[0], range_x[1])
    dest_y = random.randint(range_y[0], range_y[1])
    destination = get_closet_road_node(dest_x, dest_y, graph)
    return destination


def get_distance(coordsA, coordsB):
    xA, yA = coordsA
    xB, yB = coordsB
    return math.pow(xB - xA, 2) + math.pow(yB - yA, 2)


if __name__ == "__main__":
    obstacles_s = get_obstacles(obstacles)
    grid_c = 50  # Replace with the desired grid count
    road_nodes = get_roads_nodes()
    # print(obstacles_s)
    # graph_i = build_graph(obstacles_s, grid_c)
    # print(*graph_i, sep="\n", end="\n\n")
    # graph_cache = get_graph()
    # print(*graph_cache, sep="\n", end="\n\n")
