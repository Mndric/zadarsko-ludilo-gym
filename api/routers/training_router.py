from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import get_current_user
from repositories.training_repository import TrainingRepository
from services.training_service import TrainingService

router = APIRouter(prefix="/gym", tags=["Zadarsko Ludilo"])

@router.post("/reserve/{equipment_id}")
async def reserve(equipment_id: int, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    repo = TrainingRepository(db)
    service = TrainingService(repo)
    return await service.process_reservation(user.id, equipment_id)
@router.post("/membership/activate")
async def activate(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    repo = TrainingRepository(db)
    service = TrainingService(repo)
    return await service.buy_membership(user.id)