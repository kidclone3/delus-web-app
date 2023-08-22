import math
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
def get_distance(coordsA, coordsB):
    xA, yA = coordsA
    xB, yB = coordsB
    return math.pow(xB - xA, 2) + math.pow(yB - yA, 2)

road_nodes = [coord for coord in get_road_nodes() if coord[0] not in ['0',str(GRID_COUNT-1)] and coord[2] not in ['0', str(GRID_COUNT-1)]]