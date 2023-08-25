import json
import os
import random
from typing import List

import orjson
import requests
import simpy
from loguru import logger

from Driver import Driver
from data.data import customers
from mdp_client import MajorDomoClient
from zeromq.client import Client
from utils import decide, road_nodes, API_URL, ZMQ_CLIENT_HOST


class Customer:
    def __init__(self, name, customer_id, list_driver:List[Driver], client, env):
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
        self.list_driver = list_driver
        self.logger = logger
        self.logger.add(f"logs/Customer.log", level="DEBUG")

    def generate_location(self):
        self.location = road_nodes[random.randint(0, len(road_nodes)-1)]
        list_drivers_location = [driver.location for driver in self.list_driver]

        while self.location in list_drivers_location:
            self.location = road_nodes[random.randint(0, len(road_nodes)-1)]
    def to_dict(self):
        return {
                    "name": self.name,
                    "customer_id": self.customer_id,
                    "active": self.active,
                    "location": f"{self.location[0]}:{self.location[1]}",
                    "destination": f"{self.destination[0]}:{self.destination[1]}",
                    "driver_id": self.driver_id
                }

    def get_new_data(self):
        response = requests.get(f"{API_URL}/customers/id", params={"customer_id": self.customer_id})
        if response.text == 'null':
            return False
        new_customer = json.loads(response.text)
        self.active = new_customer.get('active')
        self.location = list(map(int, new_customer.get('location').split(':')))
        self.destination = list(map(int, new_customer.get('destination').split(':')))
        self.driver_id = new_customer.get('driver_id')
        return True

    def update_db(self):
        data = self.to_dict()
        response = requests.post(f"{API_URL}/customers", json=data)
        logger.info(f"Update customer status: {response.json()}")

    def check_driver(self):
        if self.driver_id == None:
            data = self.to_dict()
            data['type'] = 'customer'
            self.client.send(b'matching', orjson.dumps(data))
            return False
        return True

    def run(self):
        while True:
            new_active = False
            if not self.active:
                new_active = decide(95)
            else:
                new_active = decide(5)
            if self.active:
                while self.check_driver():
                    self.update_db()
                    yield self.env.timeout(1)
                yield self.env.timeout(1)
                continue
            if self.active != new_active:
                if new_active:
                    self.generate_location()
                    yield self.env.timeout(1)
                    logger.debug(f"Customer {self.name} is activated at {self.location}")
                    self.destination = self.location
                    self.active = new_active
                    self.update_db()
                    yield self.env.timeout(1)
                    self.client.send(b'destination', orjson.dumps({
                        "work": "destination",
                        "customer_id": self.customer_id,
                        "location": f"{self.location[0]}:{self.location[1]}"
                    }))
                    yield self.env.timeout(1)
                if new_active or self.driver_id is None:
                    data = self.to_dict()
                    data['type'] = 'customer'
                    self.client.send(b'matching', orjson.dumps(data))
                    yield self.env.timeout(1)

                yield self.env.timeout(1)
            else:
                if self.active != new_active:
                    self.active = new_active
                    self.update_db()
                yield self.env.timeout(1)

            yield self.env.timeout(1)
            logger.info(f"current time {self.env.now}")
            # time.sleep(0.5)

if __name__ == "__main__":
    try:
        env = simpy.Environment()
        # env = simpy.rt.RealtimeEnvironment(factor=1)
        client = MajorDomoClient(f"tcp://{ZMQ_CLIENT_HOST}:5556", True)
        list_customers = []
        for cus in customers:
            customer_instance = Customer(cus.get('name'), cus.get('customerId'), [], client, env)
            list_customers.append(customer_instance)

        env.run(until=100)
    except Exception as e:
        logger.error(e)