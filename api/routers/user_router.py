from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db  # Pazi: sad je u core!
from schemas.user import UserCreate, UserOut
from services.user_service import UserService
from repositories.user_repository import UserRepository

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.register_user(user_in)