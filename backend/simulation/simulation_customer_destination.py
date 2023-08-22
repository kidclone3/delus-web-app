import asyncio
import json
import os
import random
import sys
import time

from Customer import Customer
from Driver import Driver
from data.data import paths

import simpy
import simpy.rt
from loguru import logger
from dotenv import load_dotenv

from zeromq.client import Client

load_dotenv()

logger.add("logs/simulation_with_customer_{time:YYYY:MM:DD:HH:MM}.log")
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")



if __name__ == "__main__":
    try:
        # env = simpy.Environment()
        env = simpy.rt.RealtimeEnvironment(factor=0.5)

        running_riders = []
        for i in range(3):
            rider = Driver(i, paths, env)
            running_riders.append(rider)
            # riders.put(rider)


        client = Client()
        list_customer = ['Alice', 'Michael', 'Kate', 'Paul', 'Susan', 'Andrew']
        running_customers = []
        for name in list_customer:
            customer = Customer(name, client, env)
            running_customers.append(customer)
            # customers.put(customer)

        env.run(until=500)
    except Exception as e:
        logger.error(e)
