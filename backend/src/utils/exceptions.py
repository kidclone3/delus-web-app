from fastapi import HTTPException
from pydantic import BaseModel


class ExceptionMessage(BaseModel):
    message: str
