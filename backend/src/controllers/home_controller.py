from fastapi import APIRouter, status

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def hello_world():
    return {"message": "Hello World!"}
