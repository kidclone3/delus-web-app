from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
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
        customer_id=customer.customer_id,
        name=customer.name,
        active=customer.active,
        location=customer.location,
        destination=customer.destination,
        driver_id=customer.driver_id
    )
    query = query.on_duplicate_key_update(
        active=query.inserted.active,
        location=query.inserted.location,
        destination=query.inserted.destination,
        driver_id=query.inserted.driver_id
    )
    try:
        await db.execute(query)
        await db.commit()
        return {"message": f"Create/Update customer {customer.name} successfully"}
    except Exception as exception:
        await db.rollback()
        raise exception


async def update_destination(customer_id: str, destination: str, db):
    query = update(Customer).where(Customer.customer_id == customer_id).values(destination=destination, active=True)
    try:
        await db.execute(query)
        await db.commit()
        return {"message": f"Update destination of customer {customer_id} to {destination} successfully"}
    except Exception as exception:
        db.rollback()
        raise exception

async def get_customer(customer_id: str, db):
    query = select(Customer).where(Customer.customer_id == customer_id)
    customer = (await db.execute(query)).scalars().first()
    return jsonable_encoder(customer)