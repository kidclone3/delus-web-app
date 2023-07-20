from src.models.olp.customer import *
from sqlalchemy.orm import Session
from src.utils.exceptions import *


async def check_duplicate_email(email: str, db: Session):
    query = select(Customer).where(Customer.email == email)
    email = (await db.execute(query)).scalars().first()
    return email


async def get_all_email(db: Session):
    query = select(Customer).limit(10)
    list_email = (await db.execute(query)).scalars().all()
    print(list_email)
    return {"data": list_email, "total": len(list_email)}


async def create_email(user: CustomerSchema, db: Session):

    check_existed = await check_duplicate_email(user.email, db)
    if check_existed:
        raise HTTPException(status_code=400, detail="Email already exists")

    query = insert(Customer).values(
        name=user.name, email=user.email, school=user.school
    )
    await db.execute(query)
    await db.commit()
    return {"message": "Create email successfully"}
