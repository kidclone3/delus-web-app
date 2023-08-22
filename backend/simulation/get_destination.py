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

def get_destination(msg):
    name = msg.get('name')
    location = msg.get('location')
    x, y = map(int, location.split(':'))
    dest_x, dest_y = generate_destination((x, y))
    dest = f"{dest_x}:{dest_y}"
    print(dest)
    return dest


if __name__ == "__main__":
    worker = Worker()
    logger.add("logs/get_destination_{time:YYYY:MM:DD:HH:MM}.log", level="DEBUG")
    while True:
        try:
            msg = worker.receive()
            if msg is None:
                continue
            if msg.get('type') == 'health_check':
                worker.send({"status": "ok"})
            else:
                logger.info(f"Received name: {msg.get('name')}")
                destination = get_destination(msg)
                logger.info(f"Destination: {destination}")
                # logger.info(f"Destination: {destination}")
                request = requests.post(url="http://localhost:8005/customers/update_destination", params={
                    "name": msg.get('name'),
                    "destination": destination
                })
                logger.info(f"Response: {request.json()}")

        except Exception as e:
            time.sleep(1)
            continue
