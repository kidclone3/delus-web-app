import json
import random

import requests
import simpy
from fastapi.encoders import jsonable_encoder
from loguru import logger
from data.data import drivers
from utils import road_nodes, API_URL
from zeromq.client import Client


class Driver:
    def __init__(self, name:str, driver_id:str, client: Client, env):
        self.name = name
        self.driver_id = driver_id
        self.status = 'idle'
        self.location = road_nodes[random.randint(0, len(road_nodes)-1)]
        dummy_path = [self.location]
        self.path = dummy_path
        self.path_index = 0
        self.customer_id = None

        self.client = client
        self.env = env
        self.env.process(self.run(self.env))
        # self.run(self.env)

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
    def get_new_data(self):
        response = requests.get(f"{API_URL}/drivers/id", params={"driver_id": self.driver_id})
        if response.text == 'null':
            return False
        new_driver = json.loads(response.text)
        self.status = new_driver.get('status')
        self.location = list(map(int, new_driver.get('location').split(':')))
        self.path = json.loads(new_driver.get('path'))
        self.path_index = new_driver.get('path_index')
        self.customer_id = new_driver.get('customer_id')
        return True
    def update_db(self):
        data = self.to_dict()
        response = requests.post(f"{API_URL}/drivers", json=jsonable_encoder(data))

    def get_customer_location(self, location='location'):
        response = requests.get(f"{API_URL}/customers/id", params={"customer_id": self.customer_id})
        customer = json.loads(response.text)
        return list(map(int, customer.get(location).split(':')))
    def run(self, env):
        while True:
            if self.status == 'idle': # Wait for matching
                flag = self.get_new_data()
                if not flag:
                    data = self.to_dict()
                    response = requests.post(f"{API_URL}/drivers", json=jsonable_encoder(data))
                    logger.info(f"Create new driver status: {response.json()}")

                    self.update_db()
                    yield self.env.timeout(1)
                logger.info(f"Driver {self.name} is idle")

                msg = self.to_dict()
                msg['work'] = 'matching'
                msg['type'] = 'driver'
                self.client.send(msg=msg)

                yield env.timeout(1)
                continue
            if self.status == 'pickup':
                # get customer location:
                customer_location = self.get_customer_location()
                msg = self.to_dict()
                msg['work'] = 'route'
                msg['destination'] = f"{customer_location[0]}:{customer_location[1]}"
                self.client.send(msg=msg)
                # wait for customer to get in
                flag = self.get_new_data()
                while not flag or len(self.path) == 1:
                    flag = self.get_new_data()
                    yield env.timeout(1)

                for i in range(len(self.path)):
                    self.location = self.path[i]
                    self.path_index = i
                    self.update_db()
                    yield env.timeout(1)

            #     when customer get in
                if self.location == self.path[-1]:
                    yield env.timeout(5) # wait for customer to get in
                    self.status = 'enroute'
                    self.update_db()

                yield env.timeout(1)
                continue
            if self.status == 'enroute':
                destination_location = self.get_customer_location('destination')
                # remove customer
                self.change_customer_active()

                msg = self.to_dict()
                msg['work'] = 'route'
                msg['destination'] = f"{destination_location[0]}:{destination_location[1]}"

                self.client.send(msg=msg)
                flag = self.get_new_data()
                while not flag:
                    flag = self.get_new_data()
                    yield env.timeout(1)
                for i in range(len(self.path)):
                    self.location = self.path[i]
                    self.path_index = i
                    self.update_db()
                    yield env.timeout(1)

                if self.location == self.path[-1]:
                    yield env.timeout(5) # wait for customer to get out
                    self.status = 'idle'
                    self.customer_id = None
                    self.update_db()
                    self.remove_customer()
            # sleep(0.15)
            yield env.timeout(1)

    def remove_customer(self):
#         delete customer by id
        response = requests.delete(f"{API_URL}/customers/id", params={"customer_id": self.customer_id})
        logger.info(f"Delete customer: {response.json()}")

    def change_customer_active(self):
        response = requests.put(f"{API_URL}/customers/id", params={"customer_id": self.customer_id, 'active': False})
        logger.info(f"Change customer active: {response.json()}")

if __name__ == "__main__":
    try:
        # env = simpy.Environment()
        env = simpy.rt.RealtimeEnvironment(factor=1)
        logger.add("logs/Driver.log", level="DEBUG")
        running_drivers = []
        client = Client()
        for driver in drivers:
            driver_instance = Driver(driver.get('name'), driver.get('driverId'), client, env)
            running_drivers.append(driver_instance)

        env.run(until=100)
    except Exception as e:
        logger.error(e)