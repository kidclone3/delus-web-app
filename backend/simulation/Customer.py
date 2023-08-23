import os
import random

import requests
import simpy
from loguru import logger

from data.data import customers
from zeromq.client import Client
from utils import decide, road_nodes
class Customer:
    def __init__(self, name, customer_id, client, env):
        self.refreshInterval = 200
        self.name = name
        self.customer_id = customer_id
        self.active = False
        self.location = None
        self.destination = None
        self.driver_id = None
        self.env = env
        self.client = client
        self.env.process(self.run())
    def to_dict(self):
        return {
                    "name": self.name,
                    "customer_id": self.customer_id,
                    "active": self.active,
                    "location": f"{self.location[0]}:{self.location[1]}",
                    "destination": f"{self.destination[0]}:{self.destination[1]}",
                    "driver_id": self.driver_id
                }
    def run(self):
        # get the pid for the current process
        while True:
            new_active = False
            if self.active:
                new_active = decide(95)
            else:
                # new_active = decide(5)
                new_active = True

            if self.active != new_active:
                if new_active:
                    location = road_nodes[random.randint(0, len(road_nodes)-1)]
                    self.location = location
                    logger.debug(f"Customer {self.name} is activated at {location}")
                    self.destination = location

                self.active = new_active

                # create post request to create/update customer without async
                response = requests.post("http://localhost:8005/customers", json=self.to_dict())
                logger.debug(f"Customer {self.name} is activated: {self.active}")
                logger.info(f"Response: {response.json()}")
                self.client.send({
                    "customer_id": self.customer_id,
                    "location": f"{self.location[0]}:{self.location[1]}"
                })

            yield self.env.timeout(5)
            # time.sleep(0.5)

if __name__ == "__main__":
    try:
        env = simpy.Environment()
        # env = simpy.rt.RealtimeEnvironment(factor=0.5)
        client = Client()
        list_customers = []
        for cus in customers:
            customer_instance = Customer(cus.get('name'), cus.get('customerId'), client, env)
            list_customers.append(customer_instance)

        env.run(until=10)
    except Exception as e:
        logger.error(e)