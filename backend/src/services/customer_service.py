from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.customers import Customer


async def get_all_customers(db: Session):
    query = select(Customer)
    list_customers = (await db.execute(query)).scalars().all()
    return {
        'data': jsonable_encoder(list_customers),
        'total': len(list_customers)
    }
