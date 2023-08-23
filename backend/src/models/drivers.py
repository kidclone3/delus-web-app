import uuid
from enum import IntEnum
from typing import Optional

from sqlalchemy import *

from src.models import BaseModel
from src.utils.utils import ORJSONModel


class Driver(BaseModel):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True)
    driver_id = Column(BINARY(length=16), unique=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    status = Column(Integer, default=True)
    location = Column(String(5), nullable=False)
    path = Column(Text(), nullable=True)
    path_index = Column(Integer, nullable=True)
    customer_id = Column(BINARY(length=16), unique=True, default=uuid.uuid4)

class DriverStatusEnum(IntEnum):
    idle = 0
    pickup = 1
    enroute = 2

class DriverSchema(ORJSONModel):
    id: Optional[int]
    driver_id: Optional[str]
    name: str
    status: DriverStatusEnum = DriverStatusEnum.idle
    location: str
    path: str
    path_index: int
    customer_id: str

class ListDriverSchema(ORJSONModel):
    data: list[DriverSchema]
    total: int


