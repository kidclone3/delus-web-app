from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.models import get_session

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_email(
    db: Session = Depends(get_session),
):
    try:
        pass
    except HTTPException as exception:
        message_exception = exception.detail
        return {"message": message_exception}
