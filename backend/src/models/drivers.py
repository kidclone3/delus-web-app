import uuid

from sqlalchemy import *

from src.models import BaseModel
from src.utils.utils import ORJSONModel

from pydantic import EmailStr


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


class DriverSchema(ORJSONModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    password: str
    license_number: str


class ListDriverSchema(ORJSONModel):
    data: list[DriverSchema]
    total: int
