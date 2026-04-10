from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(models.User).where(models.User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user_data: dict):
        new_user = models.User(**user_data)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user