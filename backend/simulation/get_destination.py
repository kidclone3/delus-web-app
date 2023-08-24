import time
from hashlib import md5

import requests

from methods import *
queue = []
from zeromq.worker import Worker
from loguru import logger

def push_message(data):
    global queue
    queue.append(data)

def get_destination(location):
    x, y = map(int, location.split(':'))
    dest_x, dest_y = generate_destination((x, y))
    dest = f"{dest_x}:{dest_y}"
    return dest


if __name__ == "__main__":
    worker = Worker()
    logger.add("logs/get_destination.log", level="DEBUG")
    while True:
        try:
            msg = worker.receive()
            if msg is None:
                continue

            if msg.get('work') != 'destination':
                continue
            else:
                destination = get_destination(msg.get('location'))
                logger.info(f"Destination: {destination}")
                request = requests.post(url="http://localhost:8005/customers/update_destination", params={
                    "customer_id": msg.get('customer_id'),
                    "destination": destination
                })
                logger.info(f"Update destination: {request.json()}")

            time.sleep(0.8)
        except Exception as e:
            time.sleep(0.8)
