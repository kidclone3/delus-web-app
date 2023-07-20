from fastapi import APIRouter, Depends, status, HTTPException

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_api_feature():
    try:
        pass
    except HTTPException as exception:
        message_exception = exception.detail
        return {"message": message_exception}
