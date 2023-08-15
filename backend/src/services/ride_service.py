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


async def create_ride(ride: RideSchema, db: Session):
    query = upsert(Ride).values(
        car_id=ride.car_id,
        location=ride.location,
        path=ride.path,
    )
    query = query.on_duplicate_key_update(
        location = query.inserted.location,
    )
    try:
        await db.execute(query)
        await db.commit()
        return {"message": "Create ride successfully"}
    except Exception as exception:
        await db.rollback()
        raise exception
