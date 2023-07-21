from fastapi import APIRouter, status, UploadFile, File, Depends
from sqlalchemy.orm import Session
from src.services import home_service
from src.models import get_session

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def hello_world():
    return {"message": "Hello World!"}

@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_file(
        file: UploadFile = File(...),
        db: Session = Depends(get_session)
):
    status = await home_service.upload_file(file, db)
    return status
    # return {"message": "Upload file!"}