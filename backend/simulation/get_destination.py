import time
from concurrent import futures

import grpc
import orjson
import requests

from methods import *
from test_grpc import get_destination_pb2_grpc, get_destination_pb2
from utils import ZMQ_SERVER_HOST, API_URL

from loguru import logger


# def get_destination(location):
#     x, y = map(int, location.split(':'))
#     dest_x, dest_y = generate_destination((x, y))
#     dest = f"{dest_x}:{dest_y}"
#     return dest
#
#
# def update_destination(customer_id, new_destination):
#     response = requests.post(f"{API_URL}/customers/update_destination", params={
#         'customer_id': customer_id,
#         'destination': new_destination
#     })
#     logger.info(f"Update destination: {response.json()}")

class Destination(
    get_destination_pb2_grpc.GetDestinationServicer
):
    def GetDestination(self, request, context):
        if not request.pos_x or not request.pos_y:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid argument")
        logger.info(f"Get destination for customer at {request.pos_x}:{request.pos_y}")
        dest_x, dest_y = generate_destination((request.pos_x, request.pos_y))
        logger.info(f"Destination: {dest_x}:{dest_y}")
        return get_destination_pb2.Destination(pos_x=dest_x, pos_y=dest_y)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    get_destination_pb2_grpc.add_GetDestinationServicer_to_server(Destination(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logger.add("logs/get_destination.log", level="DEBUG")
    serve()
