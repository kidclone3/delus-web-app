from sqlalchemy import *

from src.models import BaseModel


class Customer(BaseModel):
    __tablename__ = "olp_customer"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    school = Column(String(255), nullable=True)
