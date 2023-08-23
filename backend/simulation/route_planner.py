import time

from loguru import logger

from zeromq.worker import Worker
from utils import directions
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




if __name__ == "__main__":
    logger.add("logs/route_planner.log", level="DEBUG")

    start_position = (85,79)
    destination = (43,28)
    path = get_shortest_path(start_position, destination)
    logger.info(f"Path: {path}")
    # worker = Worker()
    # while True:
    #     try:
    #         msg = worker.receive()
    #         if msg is None:
    #             continue
    #         elif msg.get('work') != 'route':
    #             continue
    #         else:
    #             # msg = driver dict
    #             del msg['work']
    #             start_position = msg.get('location')
    #             destination = msg.get('destination')
    #             path = get_shortest_path(start_position, destination)
    #             logger.info(f"Path: {path}")
    #
    #     except Exception as e:
    #         time.sleep(1)

