from typing import Optional

from sqlalchemy import *
from sqlalchemy.orm import Mapped

from src.models import BaseModel
from src.utils.utils import ORJSONModel


class Customer(BaseModel):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)
    location = Column(String(255), nullable=False)


class CustomerSchema(ORJSONModel):
    name: str
    active: bool
    location: str


class ListCustomerSchema(ORJSONModel):
    data: list[CustomerSchema]
    total: int
