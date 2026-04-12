from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import get_current_user, check_admin
from schemas.training import EquipmentCreate, EquipmentOut, EquipmentUpdate, ReservationOut, MembershipOut
from repositories.training_repository import TrainingRepository
from services.training_service import TrainingService

router = APIRouter(prefix="/gym", tags=["Zadarsko Ludilo - Teretana"])


@router.post("/equipment", response_model=EquipmentOut, status_code=status.HTTP_201_CREATED)
async def create_equipment(payload: EquipmentCreate, db: AsyncSession = Depends(get_db), admin=Depends(check_admin)):
    repo = TrainingRepository(db)
    return await repo.create_equipment(payload.name, payload.quantity)

@router.get("/equipment", response_model=List[EquipmentOut])
async def list_equipment(db: AsyncSession = Depends(get_db)):
    repo = TrainingRepository(db)
    return await repo.get_all_equipment()

@router.get("/equipment/{id}", response_model=EquipmentOut)
async def get_equipment(id: int, db: AsyncSession = Depends(get_db)):
    repo = TrainingRepository(db)
    eq = await repo.get_equipment_by_id(id)
    if not eq:
        raise HTTPException(status_code=404, detail="Oprema ne postoji")
    return eq


@router.post("/reserve/{equipment_id}", status_code=status.HTTP_201_CREATED)
async def reserve_equipment(equipment_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    repo = TrainingRepository(db)
    service = TrainingService(repo)
    return await service.process_reservation(user.id, equipment_id)

@router.get("/my-reservations", response_model=List[ReservationOut])
async def my_reservations(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = TrainingRepository(db)
    return await repo.get_user_reservations(user.id)

@router.delete("/reservations/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_reservation(id: int, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = TrainingRepository(db)
    # Ovdje provjeravamo ownership (korisnik briše samo svoje)
    success = await repo.delete_user_reservation(id, user.id)
    if not success:
        raise HTTPException(status_code=403, detail="Ne možete otkazati tuđu rezervaciju ili rezervacija ne postoji")
    return None


@router.post("/membership/activate", response_model=MembershipOut)
async def activate_membership(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = TrainingRepository(db)
    service = TrainingService(repo)
    return await service.buy_membership(user.id)