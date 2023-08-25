import dotenv

dotenv.load_dotenv()
import os

LOG_FOLDER = os.getenv("LOG_FOLDER", ".")
CLIENT_HOST = os.getenv("ZMQ_CLIENT_HOST")
CLIENT_PORT = os.getenv("ZMQ_CLIENT_PORT")
SERVER_HOST = os.getenv("ZMQ_SERVER_HOST")
SERVER_PORT = os.getenv("ZMQ_SERVER_PORT")
