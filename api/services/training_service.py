from fastapi import HTTPException, status
from repositories.training_repository import TrainingRepository
from models.user import Reservation, User  # Dodala si User ovdje za provjeru role
from datetime import datetime
from sqlalchemy import select

class TrainingService:
    def __init__(self, repo: TrainingRepository):
        self.repo = repo

    async def buy_membership(self, user_id: int):
        existing = await self.repo.get_membership(user_id)
        if existing:
            raise HTTPException(status_code=400, detail="Već imaš aktivnu članarinu!")
        return await self.repo.activate_membership(user_id)

    async def process_reservation(self, user_id: int, equipment_id: int):
      
        result = await self.repo.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Korisnik nije pronađen!")

        if not user.is_admin:  
            membership = await self.repo.get_membership(user_id)
            if not membership:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Pristup odbijen. Nemaš aktivnu članarinu!"
                )

        equipment = await self.repo.get_equipment_by_id(equipment_id)
        if not equipment:
            raise HTTPException(status_code=404, detail="Sprava ne postoji!")
        
        if equipment.quantity <= 0:
            raise HTTPException(status_code=400, detail="Sva oprema ovog tipa je trenutno zauzeta!")

        equipment.quantity -= 1
        new_res = Reservation(
            user_id=user_id, 
            equipment_id=equipment_id, 
            reservation_date=datetime.utcnow()  
        )
        
        return await self.repo.create_reservation(new_res)