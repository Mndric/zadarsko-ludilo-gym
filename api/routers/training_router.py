from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from core.security import get_current_user, check_admin # Pazi da imaš check_admin u security.py
from models.user import User, Equipment, Reservation, Membership
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/gym", tags=["Gym Operations"])

class EquipmentCreate(BaseModel):
    name: str
    quantity: int

@router.get("/equipment")
async def get_all_equipment(db: AsyncSession = Depends(get_db)):
    """Prikazuje svu opremu u Zadarskom Ludilu."""
    result = await db.execute(select(Equipment))
    return result.scalars().all()

@router.post("/equipment", status_code=status.HTTP_201_CREATED)
async def add_equipment(
    eq_in: EquipmentCreate, 
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(check_admin) # SAMO ADMIN
):
    """Samo korisnik s is_admin=True može dodati sprave."""
    new_eq = Equipment(name=eq_in.name, quantity=eq_in.quantity)
    db.add(new_eq)
    await db.commit()
    await db.refresh(new_eq)
    return new_eq

@router.post("/reserve/{equipment_id}")
async def create_reservation(
    equipment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rezervacija sprave za ulogiranog korisnika."""
    equipment = await db.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Sprava ne postoji!")

    new_res = Reservation(
        user_id=current_user.id,
        equipment_id=equipment_id,
        reservation_date=datetime.utcnow()
    )
    db.add(new_res)
    await db.commit()
    return {"status": "success", "message": f"Rezervirano: {equipment.name}"}