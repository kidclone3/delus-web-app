import time

import orjson
import requests

from mdp_worker import MajorDomoWorker
from methods import *
from utils import ZMQ_SERVER_HOST, API_URL

from loguru import logger


def get_destination(location):
    x, y = map(int, location.split(':'))
    dest_x, dest_y = generate_destination((x, y))
    dest = f"{dest_x}:{dest_y}"
    return dest


def update_destination(customer_id, new_destination):
    response = requests.post(f"{API_URL}/customers/update_destination", params={
        'customer_id': customer_id,
        'destination': new_destination
    })
    logger.info(f"Update destination: {response.json()}")


if __name__ == "__main__":
    worker = MajorDomoWorker(f"tcp://{ZMQ_SERVER_HOST}:5556", b"destination", True)
    logger.add("logs/get_destination.log", level="DEBUG")
    reply = None
    while True:
        try:
            msg = worker.recv(reply)
            msg = orjson.loads(msg[0])
            destination = get_destination(msg.get('location'))
            logger.info(f"Destination: {destination}")
            update_destination(msg.get('customer_id'), destination)
            reply = [bytes(destination, 'utf-8')]

        except Exception as e:
            time.sleep(0.1)
