from pydantic import EmailStr
from sqlalchemy import *

from src.models import BaseModel
from src.utils.utils import ORJSONModel


class Customer(BaseModel):
    __tablename__ = "olp_customer"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    school = Column(String(255), nullable=True)


class CustomerSchema(ORJSONModel):
    id: int
    name: str
    email: EmailStr
    school: str


class ListCustomerSchema(ORJSONModel):
    data: list[CustomerSchema]
    total: int


class ListEmailSchema(ORJSONModel):
    data: list[EmailStr]
    total: int
