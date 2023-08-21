from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from src.models import get_session
from src.models.customers import *
from src.services import customer_service

from src.utils.exceptions import ExceptionMessage

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_customers(
        db: Session = Depends(get_session),
) -> ListCustomerSchema | ExceptionMessage:
    try:
        list_customers = await customer_service.get_all_customers(db)
        return list_customers
    except HTTPException as exception:
        message_exception = exception.detail
        return {"message": message_exception}
