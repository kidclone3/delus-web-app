from typing import Any

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.models import get_session
from src.services import ride_service

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_rides(
        db: Session = Depends(get_session),
) -> dict[str, str | None] | Any:
    try:
        list_rides = await ride_service.get_all_rides(db)
        return list_rides
    except HTTPException as exception:
        message_exception = exception.detail
        return {"message": message_exception}
