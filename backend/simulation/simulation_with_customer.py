import asyncio
import json
import os
import random
import sys
import time

from data import paths

import pymysql.cursors
import simpy
import simpy.rt
import orjson
from loguru import logger
from dotenv import load_dotenv

from utils import decide, get_road_nodes

load_dotenv()

logger.add("simulation_with_customer_{time:YYYY:MM:DD:HH}.log")
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

road_nodes = [coord for coord in get_road_nodes() if coord != '0:0' and coord != '49:49']


class Customer:
    def __init__(self, name, env, conn):
        self.refreshInterval = 200
        self.name = name
        self.active = False
        self.location = None
        self.env = env
        env.process(self.run(conn))

    def run(self, conn):
        # get the pid for the current process
        pid = os.getpid()
        logger.debug(f"Customer {self.name} is running on process {pid}")
        while True:
            new_active = False
            if self.active:
                new_active = decide(5)
            else:
                new_active = decide(5)

            if self.active != new_active:
                if new_active:
                    location = road_nodes[random.randint(0, len(road_nodes)-1)]
                    self.location = location
                    logger.debug(f"Customer {self.name} is activated at {location}")

                self.active = new_active
                query = f"""
                    INSERT INTO customers (name, active, location)
                    VALUES ('{self.name}', {self.active}, '{self.location}') as new
                    ON DUPLICATE KEY UPDATE active = new.active, location = new.location;
                """
                with conn.cursor() as cursor:
                    try:
                        cursor.execute(query)
                        conn.commit()
                        logger.info(f"Customer {self.name} is activated: {self.active}")
                    except Exception as e:
                        logger.error("DB error: ", str(e))
                yield self.env.timeout(5)
            # time.sleep(0.5)


class Rider:
    def __init__(self, id, paths, conn, env):
        self.paths = paths
        self.id = id
        self.env = env
        env.process(self.run(env, conn, self.id))

    def run(self, env, conn, idx=0):

        # get the pid for the current process
        pid = os.getpid()
        logger.debug(f"Rider {self.id} is running on process {pid}")
        i = paths[idx].get('i')
        carId = paths[idx].get('carId')
        selected = paths[idx].get('selected')
        while True:
            with conn.cursor() as cursor:
                path = paths[idx].get(selected)
                x, y = path[i]
                query = f"""
                    INSERT INTO rides (car_id, location, path)
                    VALUES ('{carId}', '{x}:{y}', '{json.dumps(path)}') as new
                    ON DUPLICATE KEY UPDATE location = new.location, path = new.path;
                """
                cursor.execute(query)
                conn.commit()
                # print(await cursor.fetchall())
                logger.debug(f"Car Id: {carId}, Location: {x}:{y}")
                # time.sleep(0.15)
                yield env.timeout(1)
                if i == len(path) - 1:
                    selected = 'second' if selected == 'first' else 'first'
                    i = 0
                else:
                    i += 1


if __name__ == "__main__":
    try:
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user=DB_USER,
            password=DB_PASSWORD,
            db="delus_web",
        )
        # env = simpy.Environment()
        env = simpy.rt.RealtimeEnvironment(factor=0.2, strict=False)

        riders = simpy.Store(env, capacity=3)
        for i in range(3):
            rider = Rider(i, paths, conn, env)
            # riders.put(rider)

        customers = simpy.Store(env, capacity=10)
        list_customer = ['Alice', 'Michael', 'Kate', 'Paul', 'Susan', 'Andrew']
        for name in list_customer:
            customer = Customer(name, env, conn)
            # customers.put(customer)

        env.run(until=1000)
    except Exception as e:
        logger.error(e)
