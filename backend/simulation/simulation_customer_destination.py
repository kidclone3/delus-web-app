import asyncio
import json
import os
import random
import sys
import time

from Customer import Customer
from Driver import Driver
from data.data import paths, customers, drivers

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

running_drivers = []
running_customers = []

if __name__ == "__main__":
    client = Client()
    try:
        # env = simpy.Environment()
        env = simpy.rt.RealtimeEnvironment(factor=0.5)

        for driver in drivers:
            if driver.get('name') == 'William':
                instance_driver = Driver(driver.get('name'), driver.get('driverId'), client,env)
                running_drivers.append(instance_driver)

        for cus in customers:
            if cus.get('name') == 'Paul':
                instance_customer = Customer(cus.get('name'), cus.get('customerId'), running_drivers, client, env)
                running_customers.append(instance_customer)

        env.run(until=500)
    except Exception as e:
        logger.error(e)
