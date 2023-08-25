from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.rides import Ride


async def get_all_rides(db: Session):
    query = select(Ride)
    list_rides = (await db.execute(query)).scalars().all()
    return {
        'data': jsonable_encoder(list_rides),
        'total': len(list_rides)
    }
