from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from src.models.drivers import Driver


async def get_all_drivers(db:Session):
    query = select(Driver)
    list_drivers = (await db.execute(query)).scalars().all()
    return {
        'data': jsonable_encoder(list_drivers),
        'total': len(list_drivers)
    }