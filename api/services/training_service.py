from fastapi import HTTPException, status
from repositories.training_repository import TrainingRepository
from models.user import Reservation
from datetime import datetime

class TrainingService:
    def __init__(self, repo: TrainingRepository):
        self.repo = repo

    async def process_reservation(self, user_id: int, equipment_id: int):
        membership = await self.repo.get_membership(user_id)
        if not membership:
            raise HTTPException(status_code=403, detail="Nemaš aktivnu članarinu!")

        equipment = await self.repo.get_equipment_by_id(equipment_id)
        if not equipment or equipment.quantity <= 0:
            raise HTTPException(status_code=400, detail="Sprava nije dostupna!")

        equipment.quantity -= 1
        new_res = Reservation(user_id=user_id, equipment_id=equipment_id, reservation_date=datetime.utcnow())
        
        return await self.repo.create_reservation(new_res)
    async def buy_membership(self, user_id: int):
        existing = await self.repo.get_membership(user_id)
        if existing:
            raise HTTPException(status_code=400, detail="Već imaš aktivnu članarinu!")
        
        return await self.repo.activate_membership(user_id)