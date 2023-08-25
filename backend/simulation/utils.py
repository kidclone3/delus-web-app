import os
import random

from dotenv import load_dotenv

import methods
from config import GRID_COUNT

load_dotenv()

API_URL = os.environ.get("API_URL")
ZMQ_CLIENT_HOST = os.environ.get("ZMQ_CLIENT_HOST")
ZMQ_CLIENT_PORT = os.environ.get("ZMQ_CLIENT_PORT")
ZMQ_SERVER_HOST = os.environ.get("ZMQ_SERVER_HOST")
ZMQ_SERVER_PORT = os.environ.get("ZMQ_SERVER_PORT")

def decide(percent):
    return random.randint(0, 100) < percent


road_nodes = [coord for coord in methods.get_roads_nodes() if
              coord[0] not in [0, GRID_COUNT - 1] and coord[1] not in [0, GRID_COUNT - 1]]

directions = [[1, 0],
              [-1, 0],
              [0, 1],
              [0, -1]]

if __name__ == "__main__":
    print(road_nodes)