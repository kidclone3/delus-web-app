import uuid
from enum import Enum
from typing import Optional

from sqlalchemy import *

from src.models import BaseModel
from src.utils.utils import ORJSONModel


class Driver(BaseModel):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True)
    driver_id = Column(String(36), unique=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    status = Column(String(10), default=True)
    location = Column(String(5), nullable=False)
    path = Column(Text(), nullable=True)
    path_index = Column(Integer, nullable=True)
    customer_id = Column(String(36), nullable=True, unique=True, default=uuid.uuid4)

class DriverStatusEnum(str, Enum):
    idle = 'idle'
    pickup = 'pickup'
    enroute = 'enroute'

class DriverSchema(ORJSONModel):
    id: Optional[int]
    driver_id: Optional[str]
    name: str
    status: DriverStatusEnum = DriverStatusEnum.idle
    location: str
    path: str
    path_index: int
    customer_id: Optional[str]

class ListDriverSchema(ORJSONModel):
    data: list[DriverSchema]
    total: int


