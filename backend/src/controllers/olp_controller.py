from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.models import get_session
from src.models.olp.customer import CustomerSchema, ListCustomerSchema, ListEmailSchema
from src.services import olp_handle_email

from src.utils.exceptions import ExceptionMessage

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_email(
    db: Session = Depends(get_session),
) -> ListCustomerSchema | ExceptionMessage:
    # TODO: admin check
    try:
        list_email = await olp_handle_email.get_all_email(db)
        return list_email
    except HTTPException as exception:
        message_exception = exception.detail
        return {"message": message_exception}


@router.post("/", status_code=status.HTTP_200_OK)
async def create_email(
    user: CustomerSchema,
    db: Session = Depends(get_session),
) -> ExceptionMessage:
    try:
        message = await olp_handle_email.create_email(user, db)
        return message
    except HTTPException as exception:
        message_exception = exception.detail
        return {"message": message_exception}

@router.get("/send_emails", status_code=status.HTTP_200_OK)
async def send_emails(
        db:Session = Depends(get_session)
)-> ListEmailSchema | ExceptionMessage:
    # TODO: admin check
    try:
        list_email = await olp_handle_email.send_emails(db)
        return list_email
    except HTTPException as exception:
        message_exception = exception.detail
        return {"message": message_exception}