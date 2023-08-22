import json
import os

import requests
from loguru import logger
from data.data import paths
class Driver:
    def __init__(self, id, paths, env):
        self.paths = paths
        self.id = id
        self.env = env
        env.process(self.run(env, self.id))

    def run(self, env, idx=0):

        # get the pid for the current process
        pid = os.getpid()
        logger.debug(f"Rider {self.id} is running on process {pid}")
        i = paths[idx].get('i')
        carId = paths[idx].get('carId')
        selected = paths[idx].get('selected')
        while True:
            path = paths[idx].get(selected)
            x, y = path[i]
            data = {
                "car_id": carId,
                "location": f"{x}:{y}",
                "path": json.dumps(path)
            }
            response = requests.post("http://localhost:8005/rides", json=data)
            logger.info(f"Response: {response.json()}")
            logger.debug(f"Car Id: {carId}, Location: {x}:{y}")
            # time.sleep(0.15)
            yield env.timeout(1)
            if i == len(path) - 1:
                selected = 'second' if selected == 'first' else 'first'
                i = 0
            else:
                i += 1