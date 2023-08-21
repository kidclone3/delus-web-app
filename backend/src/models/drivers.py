from sqlalchemy import *

from src.models import BaseModel
from src.utils.utils import ORJSONModel

from pydantic import EmailStr


class Driver(BaseModel):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    license_number = Column(String(255), nullable=False)


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
