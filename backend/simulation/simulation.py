import asyncio
import json
import os
import sys
import time

from data import paths

import pymysql.cursors
import simpy
import orjson
from loguru import logger

logger.add("file_{time:YYYY:MM:DD:HH}.log")
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

# DATABASE_URL = os.environ.get("DATABASE_URL")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
def run(env, conn):


    i = paths[0].get('i')

    while True:
        with conn.cursor() as cursor:
            carId = paths[0].get('carId')
            selected = paths[0].get('selected')
            path = paths[0].get(selected)
            x, y = path[i]
            query = f"""
                INSERT INTO rides (car_id, location, path)
                VALUES ('{carId}', '{x}:{y}', '{json.dumps(path)}') as new
                ON DUPLICATE KEY UPDATE location = new.location, path = new.path;
            """
            print(query)
            cursor.execute(query)
            conn.commit()
            # print(await cursor.fetchall())
            logger.debug(f"Location: {x}:{y}")
            time.sleep(2)
            yield env.timeout(1)
            if i == len(path) - 1:
                selected = 'second' if selected == 'first' else 'first'
                i = 0
            else:
                i += 1


if __name__ == "__main__":
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user=DB_USER,
        password=DB_PASSWORD,
        db="delus_web",
    )
    env = simpy.Environment()
    env.process(run(env, conn))
    env.run(until=50)