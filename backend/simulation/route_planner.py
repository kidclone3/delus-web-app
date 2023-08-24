import json
import time

import requests
from fastapi.encoders import jsonable_encoder
from loguru import logger

from zeromq.worker import Worker
from utils import directions, API_URL
from methods import get_graph

graph = get_graph()
def is_valid(x, y):
    return 0 <= x < len(graph) and 0 <= y < len(graph[0]) and graph[y][x] == 1
def get_shortest_path(start_position, destination):
#     BFS algorithm for find path
    col, row = start_position
    q = [[start_position]]
    visited = set()
    while len(q) > 0:
        path = q.pop(0)
        node = path[-1]
        x, y = node
        if (x, y) in visited:
            continue
        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if is_valid(new_x, new_y):
                q.append(path + [[new_x, new_y]])
                if new_x == destination[0] and new_y == destination[1]:
                    return path + [[new_x, new_y]]
        visited.add((x, y))

    return []


def update_db(driver):
    response = requests.post(f"{API_URL}/drivers", json=jsonable_encoder(driver))
    logger.info(f"Update drivers path: {response.json()}")


if __name__ == "__main__":
    logger.add("logs/route_planner.log", level="DEBUG")

    worker = Worker()
    while True:
        try:
            msg = worker.receive()

            if msg.get('work') != 'route':
                continue
            else:
                # msg = driver dict
                logger.info(f"From {msg.get('location')} to {msg.get('destination')}")
                del msg['work']
                start_position = list(map(int, msg.get('location').split(':')))
                destination = list(map(int, msg.get('destination').split(':')))
                del msg['destination']
                path = get_shortest_path(start_position, destination)
                msg['path'] = json.dumps(path)

                logger.info(f"Driver {msg.get('name')} has new path: {path}")
                update_db(msg)

            time.sleep(0.8)
        except Exception as e:
            time.sleep(0.8)

