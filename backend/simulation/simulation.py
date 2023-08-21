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
from dotenv import load_dotenv

load_dotenv()

logger.add("file_{time:YYYY:MM:DD:HH}.log")
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
def run(env, conn, idx=0):


    i = paths[idx].get('i')

    while True:
        with conn.cursor() as cursor:
            carId = paths[idx].get('carId')
            selected = paths[idx].get('selected')
            path = paths[idx].get(selected)
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
    id = int(sys.argv[1])
    try:
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user=DB_USER,
            password=DB_PASSWORD,
            db="delus_web",
        )
        env = simpy.Environment()
        env.process(run(env, conn, id))
        env.run(until=50)
    except Exception as e:
        logger.error(e)
