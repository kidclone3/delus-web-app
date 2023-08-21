from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert as upsert

from src.models.customers import Customer, CustomerSchema


async def get_all_customers(db: Session):
    query = select(Customer)
    list_customers = (await db.execute(query)).scalars().all()
    return {
        'data': jsonable_encoder(list_customers),
        'total': len(list_customers)
    }

async def create_customer(customer: CustomerSchema, db: Session):
    query = upsert(Customer).values(
        name=customer.name,
        active=customer.active,
        location=customer.location,
        destination=customer.destination
    )
    query = query.on_duplicate_key_update(
        active = query.inserted.active,
        location = query.inserted.location,
        destination = query.inserted.destination
    )
    try:
        await db.execute(query)
        await db.commit()
        return {"message": f"Create/Update customer {customer.name} successfully"}
    except Exception as exception:
        await db.rollback()
        raise exception