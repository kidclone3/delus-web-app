from typing import List, Optional

from sqlalchemy import *

from src.models import BaseModel
from src.utils.utils import ORJSONModel


class Ride(BaseModel):
    __tablename__ = "rides"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, nullable=False, unique=True)
    location = Column(String(255), nullable=False)
    path = Column(Text(), nullable=True)


class RideSchema(ORJSONModel):
    id: Optional[int] = None
    car_id: str
    location: str
    path: Optional[str]


class ListRideSchema(ORJSONModel):
    data: List[RideSchema]
    total: int
