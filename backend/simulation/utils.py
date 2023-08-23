import math
import os
import random

from dotenv import load_dotenv

from config import GRID_COUNT
import methods
load_dotenv()

API_URL = os.environ.get("API_URL")

def decide(percent):
    return random.randint(0, 100) < percent


road_nodes = [coord for coord in methods.get_roads_nodes() if coord[0] not in [0, GRID_COUNT-1] and coord[1] not in [0, GRID_COUNT-1]]