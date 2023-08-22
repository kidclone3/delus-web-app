import random

from config import GRID_COUNT
from data.obstacles import obstacles

def decide(percent):
    return random.randint(0, 100) < percent


def get_road_nodes():
    coords_to_obstacles = {}
    for obstacle in obstacles:
        x_start, x_end, y_start, y_end = obstacle[:4]
        x = x_start
        while x <= x_end:
            y = y_start
            while y <= y_end:
                coords_to_obstacles[f"{x}:{y}"] = True
                y += 1
            x += 1

    road_nodes = []
    for x in range(GRID_COUNT):
        for y in range(GRID_COUNT):
            if not coords_to_obstacles.get(f"{x}:{y}"):
                road_nodes.append(f"{x}:{y}")

    return road_nodes
