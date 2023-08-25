import asyncio
import json
import os
import random
import sys
import time

import pymysql

from Customer import Customer
from Driver import Driver
from data.data import paths, customers, drivers

import simpy
import simpy.rt
from loguru import logger
from dotenv import load_dotenv

from mdp_client import MajorDomoClient
from utils import ZMQ_CLIENT_HOST
from zeromq.client import Client

load_dotenv()

logger.add("logs/simulation_with_customer_{time:YYYY:MM:DD:HH:MM}.log")
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

running_drivers = []
running_customers = []

if __name__ == "__main__":
    conn = pymysql.connect(host="localhost", user=DB_USER, password=DB_PASSWORD, db="delus_web")
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM drivers")
        cursor.execute("DELETE FROM customers")
        conn.commit()
        logger.info("Delete all drivers and customers")
        conn.close()


    try:
        # env = simpy.Environment()
        env = simpy.rt.RealtimeEnvironment(factor=0.8)

        for driver in drivers:
            client = MajorDomoClient(f"tcp://localhost:5556", False)
            # if driver.get('name') == 'William':
            instance_driver = Driver(driver.get('name'), driver.get('driverId'), client, env)
            running_drivers.append(instance_driver)

        for cus in customers:
            # if cus.get('name') == 'Paul':
            client = MajorDomoClient(f"tcp://localhost:5556", False)
            instance_customer = Customer(cus.get('name'), cus.get('customerId'), running_drivers, client, env)
            running_customers.append(instance_customer)

        env.run(until=1000)
    except Exception as e:
        logger.error(e)
