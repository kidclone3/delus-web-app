from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert as upsert
from sqlalchemy.orm import Session

from src.models.drivers import Driver, DriverSchema


async def get_all_drivers(db: Session):
    query = select(Driver)
    list_drivers = (await db.execute(query)).scalars().all()
    return {
        'data': jsonable_encoder(list_drivers),
        'total': len(list_drivers)
    }


async def create_driver(driver: DriverSchema, db: Session):
    query = upsert(Driver).values(
        driver_id=driver.driver_id,
        name=driver.name,
        status=driver.status,
        location=driver.location,
        path=driver.path,
        path_index=driver.path_index,
        customer_id=driver.customer_id
    )
    query = query.on_duplicate_key_update(
        location=query.inserted.location,
        path_index=query.inserted.path_index,
        path=query.inserted.path,
        status=query.inserted.status,
        customer_id=query.inserted.customer_id
    )
    try:
        await db.execute(query)
        await db.commit()
        return {"message": "Create/Update customer successfully"}
    except Exception as exception:
        await db.rollback()
        raise exception


async def get_driver(driver_id: str, db: Session):
    query = select(Driver).where(Driver.driver_id == driver_id)
    driver = (await db.execute(query)).scalars().first()
    return jsonable_encoder(driver)
