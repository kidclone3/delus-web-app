import json
import os
import random

import requests
import simpy
from fastapi.encoders import jsonable_encoder
from loguru import logger
from data.data import paths, drivers
from utils import road_nodes, API_URL


class Driver:
    def __init__(self, name, driver_id, env):
        self.paths = paths
        self.name = name
        self.driver_id = driver_id
        self.status = 'enroute'
        self.location = road_nodes[random.randint(0, len(road_nodes)-1)]
        dummy_path = [self.location, [self.location[0]+1, self.location[1]]]
        self.path = dummy_path
        self.path_index = 0
        self.customer_id = None

        self.env = env
        self.env.process(self.run(self.env))

    def to_dict(self):
        return {
            "name": self.name,
            "driver_id": self.driver_id,
            "status": self.status,
            "location": f"{self.location[0]}:{self.location[1]}",
            "path": json.dumps(self.path),
            "path_index": self.path_index,
            "customer_id": self.customer_id
        }

    def run(self, env):


        while True:

            data = self.to_dict()
            response = requests.post(f"{API_URL}/drivers", json=jsonable_encoder(data))
            logger.info(f"Response: {response.json()}")
            logger.debug(f"Driver Id: {self.name}, Location: {self.location}")
            # time.sleep(0.15)
            yield env.timeout(1)
            # if i == len(path) - 1:
            #     selected = 'second' if selected == 'first' else 'first'
            #     i = 0
            # else:
            #     i += 1

if __name__ == "__main__":
    try:
        # env = simpy.Environment()
        env = simpy.rt.RealtimeEnvironment(factor=0.5)

        running_riders = []
        for driver in drivers:
            driver_instance = Driver(driver.get('name'), driver.get('driverId'), env)
            running_riders.append(driver_instance)

        env.run(until=100)
    except Exception as e:
        logger.error(e)