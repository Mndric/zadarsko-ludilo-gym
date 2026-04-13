from fastapi import HTTPException, status
from repositories.training_repository import TrainingRepository
from models.user import Reservation, User
from datetime import datetime
from sqlalchemy import select
from schemas.training import ReservationCreate

class TrainingService:
    def __init__(self, repo: TrainingRepository):
        self.repo = repo

    async def buy_membership(self, user_id: int):
        existing = await self.repo.get_membership(user_id)
        if existing:
            raise HTTPException(status_code=400, detail="Već imaš aktivnu članarinu!")
        return await self.repo.activate_membership(user_id)

    async def process_reservation(self, user_id: int, reservation_data: ReservationCreate):
      
        result = await self.repo.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Korisnik nije pronađen!")

        if reservation_data.reservation_date.replace(tzinfo=None) < datetime.utcnow():
            raise HTTPException(
                status_code=400, 
                detail="Ne možete rezervirati termin u prošlosti!"
            )

        if not user.is_admin:  
            membership = await self.repo.get_membership(user_id)
            if not membership:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Pristup odbijen. Nemaš aktivnu članarinu!"
                )

        equipment = await self.repo.get_equipment_by_id(reservation_data.equipment_id)
        if not equipment:
            raise HTTPException(status_code=404, detail="Sprava ne postoji!")
        
        if equipment.quantity <= 0:
            raise HTTPException(status_code=400, detail="Sva oprema ovog tipa je trenutno zauzeta!")

        equipment.quantity -= 1
        
        new_res = Reservation(
            user_id=user_id, 
            equipment_id=reservation_data.equipment_id, 
            reservation_date=reservation_data.reservation_date
        )
        
        return await self.repo.create_reservation(new_res)

    async def get_reservation_details(self, reservation_id: int, user_id: int):
        reservation = await self.repo.get_reservation_by_id(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Rezervacija nije pronađena")
        
        # Ključni dio za obranu: Provjera ownershipa (vlasništva)
        if reservation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Nemate pristup tuđoj rezervaciji"
            )
        return reservation

    async def update_reservation(self, reservation_id: int, user_id: int, new_date: datetime):
        reservation = await self.get_reservation_details(reservation_id, user_id)
        
        if new_date.replace(tzinfo=None) < datetime.utcnow():
            raise HTTPException(
                status_code=400, 
                detail="Novi datum ne može biti u prošlosti"
            )
        
        return await self.repo.update_reservation_date(reservation, new_date)