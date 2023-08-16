from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from src.models import get_session
from src.models.drivers import DriverSchema, ListDriverSchema
from src.services import driver_service

from src.utils.exceptions import ExceptionMessage

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_drivers(
    db: Session = Depends(get_session),
) -> ListDriverSchema | ExceptionMessage:
    try:
        list_drivers = await driver_service.get_all_drivers(db)
        print(list_drivers)
        return list_drivers
    except HTTPException as exception:
        message_exception = exception.detail
        return {"message": message_exception}