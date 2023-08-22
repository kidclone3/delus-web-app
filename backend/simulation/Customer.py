import os
import random

import requests
from loguru import logger
from utils import decide, get_road_nodes, road_nodes
class Customer:
    def __init__(self, name, client, env):
        self.refreshInterval = 200
        self.name = name
        self.active = False
        self.location = None
        self.destination = None
        self.env = env
        self.client = client
        env.process(self.run())

    def run(self):
        # get the pid for the current process
        pid = os.getpid()
        logger.debug(f"Customer {self.name} is running on process {pid}")
        while True:
            new_active = False
            if self.active:
                new_active = decide(95)
            else:
                new_active = decide(5)

            if self.active != new_active:
                if new_active:
                    location = road_nodes[random.randint(0, len(road_nodes)-1)]
                    self.location = location
                    logger.debug(f"Customer {self.name} is activated at {location}")

                self.active = new_active

                # create post request to create/update customer without async
                data = {
                    "name": self.name,
                    "active": self.active,
                    "location": self.location,
                }
                response = requests.post("http://localhost:8005/customers", json=data)
                logger.debug(f"Customer {self.name} is activated: {self.active}")
                logger.info(f"Response: {response.json()}")
                self.client.send(data)

            yield self.env.timeout(5)
            # time.sleep(0.5)
