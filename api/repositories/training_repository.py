from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import Equipment, Reservation, Membership

class TrainingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_membership(self, user_id: int):
        result = await self.db.execute(select(Membership).where(Membership.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_equipment_by_id(self, eq_id: int):
        return await self.db.get(Equipment, eq_id)

    async def create_reservation(self, reservation: Reservation):
        self.db.add(reservation)
        await self.db.commit()
        await self.db.refresh(reservation)
        return reservation
    async def activate_membership(self, user_id: int):
        new_membership = Membership(
            user_id=user_id, 
            start_date=datetime.utcnow()
        )
        self.db.add(new_membership)
        await self.db.commit()
        return new_membership