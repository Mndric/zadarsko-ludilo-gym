from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.user import Equipment, Reservation, Membership
from datetime import datetime

class TrainingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_equipment(self, name: str, quantity: int):
        new_eq = Equipment(name=name, quantity=quantity)
        self.db.add(new_eq)
        await self.db.commit()
        await self.db.refresh(new_eq)
        return new_eq

    async def get_all_equipment(self):
        result = await self.db.execute(select(Equipment))
        return result.scalars().all()

    async def get_equipment_by_id(self, eq_id: int):
        return await self.db.get(Equipment, eq_id)

    async def get_membership(self, user_id: int):
        result = await self.db.execute(select(Membership).where(Membership.user_id == user_id))
        return result.scalar_one_or_none()

    async def activate_membership(self, user_id: int):
    # Dodajemo 'type="Standard"' jer tvoja baza ne dopušta prazno polje
        new_membership = Membership( user_id=user_id, type="Standard", start_date=datetime.utcnow())
        self.db.add(new_membership)
        await self.db.commit()
        await self.db.refresh(new_membership) 
        return new_membership

    async def create_reservation(self, reservation: Reservation):
        self.db.add(reservation)
        await self.db.commit()
        await self.db.refresh(reservation)
        return reservation

    async def get_user_reservations(self, user_id: int):
        result = await self.db.execute(select(Reservation).where(Reservation.user_id == user_id))
        return result.scalars().all()

    async def delete_user_reservation(self, res_id: int, user_id: int):
        result = await self.db.execute(
            select(Reservation).where(Reservation.id == res_id, Reservation.user_id == user_id)
        )
        res = result.scalar_one_or_none()
        if res:
            equipment = await self.db.get(Equipment, res.equipment_id)
            if equipment:
                equipment.quantity += 1
            
            await self.db.delete(res)
            await self.db.commit()
            return True
        return False