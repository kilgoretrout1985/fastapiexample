from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from . import models, schemas


async def get_user(db: AsyncSession, user_id: int):
    results = await db.execute(
        # selectinload because no lasy loading is allowed in async mode
        select(models.User).filter(models.User.id == user_id).options(selectinload(models.User.items))
    )
    return results.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    results = await db.execute(
        select(models.User).filter(models.User.email == email).options(selectinload(models.User.items))
    )
    return results.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    results = await db.execute(
        select(models.User).offset(skip).limit(limit).options(selectinload(models.User.items))
    )
    return results.scalars().all()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, items=[])
    db.add(db_user)
    await db.commit()
    # TODO: this commented line breaks everything because of .items relationship
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    # await db.refresh(db_user, attribute_names=['id', 'items'])
    return db_user


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    results = await db.execute(
        select(models.Item).offset(skip).limit(limit)
    )
    return results.scalars().all()


async def create_user_item(db: AsyncSession, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
