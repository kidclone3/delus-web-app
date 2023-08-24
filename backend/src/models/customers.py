import uuid
from typing import Optional

from sqlalchemy import *

from src.models import BaseModel
from src.utils.utils import ORJSONModel
from pydantic import UUID4


class Customer(BaseModel):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(36), unique=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)
    location = Column(String(5), nullable=False)
    destination = Column(String(5), nullable=True)
    driver_id = Column(String(36),nullable=True, unique=True, default=uuid.uuid4)


class CustomerSchema(ORJSONModel):
    id: Optional[int]
    customer_id: Optional[str]
    name: str
    active: bool
    location: str
    destination: Optional[str]
    driver_id: Optional[str]


class ListCustomerSchema(ORJSONModel):
    data: list[CustomerSchema]
    total: int
