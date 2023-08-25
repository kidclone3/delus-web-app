import json
import time

import orjson
import requests
from fastapi.encoders import jsonable_encoder
from loguru import logger

from methods import get_distance
from utils import API_URL, ZMQ_SERVER_HOST, ZMQ_SERVER_PORT
from zeromq.mdp_worker import MajorDomoWorker

if __name__ == "__main__":
    logger.add("logs/matching_pair.log", level="INFO")
    driver_queue = []
    driver_id_set = set()
    customer_queue = []
    customer_id_set = set()

    worker_reset = MajorDomoWorker(f"tcp://{ZMQ_SERVER_HOST}:5556", b"reset", True)

    worker = MajorDomoWorker(f"tcp://{ZMQ_SERVER_HOST}:5556", b"matching", True)
    reply = None
    while True:
        try:
            msg = worker.recv(reply)

            msg = orjson.loads(msg[0])
            if msg.get('type') == 'driver':
                if msg.get('driver_id') in driver_id_set:
                    continue
                del msg['type']
                logger.info(f"Driver {msg.get('name')} is waiting for matching")
                driver_queue.append(msg)
                driver_id_set.add(msg.get('driver_id'))
                reply = [b"Done"]
            elif msg.get('type') == 'customer':
                if msg.get('customer_id') in customer_id_set:
                    continue
                del msg['type']
                logger.info(f"Customer {msg.get('name')} is waiting for matching")
                customer_queue.append(msg)
                customer_id_set.add(msg.get('customer_id'))
                reply = [b"Done"]

            while len(driver_queue) > 0 and len(customer_queue) > 0:
                logger.debug(f"len driver_queue: {len(driver_queue)}")
                logger.debug(f"len customer_queue: {len(customer_queue)}")
                customer = customer_queue.pop()
                customer_location = list(map(int, customer.get('location').split(':')))
                driver_queue.sort(key=lambda x: get_distance(list(map(int, x.get('location').split(':'))), customer_location))
                driver = driver_queue.pop()

                logger.info(f"""
                Customer: {customer.get('name')} matched with driver: {driver.get('name')} 
                with distance: {get_distance(list(map(int, driver.get('location').split(':'))), customer_location)}
                """)

                driver['status'] = 'pickup'
                driver['customer_id'] = customer.get('customer_id')
                customer['driver_id'] = driver.get('driver_id')

                response_driver = requests.post(f"{API_URL}/drivers", json=jsonable_encoder(driver))
                logger.info(f"Update drivers: {response_driver.json()}")
                response_customer = requests.post(f"{API_URL}/customers", json=jsonable_encoder(customer))
                logger.info(f"Update customers: {response_customer.json()}")

                driver_id_set.remove(driver.get('driver_id'))
                customer_id_set.remove(customer.get('customer_id'))
                reply = [b"Done"]

        except Exception as e:
            time.sleep(0.1)