from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert
from sqlalchemy.dialects.mysql import insert as upsert
from sqlalchemy.orm import Session

from src.models.rides import Ride, RideSchema


async def get_all_rides(db: Session):
    query = select(Ride)
    list_rides = (await db.execute(query)).scalars().all()
    return {
        'data': jsonable_encoder(list_rides),
        'total': len(list_rides)
    }



