from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db  
from services.user_service import UserService
from schemas.user import UserCreate, UserOut
from repositories.user_repository import UserRepository
from core.security import get_current_user
from models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_user_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, 
    service: UserService = Depends(get_user_service)
):
    """
    Registracija novog korisnika. 
    Lozinka se hashira unutar servisa.
    """
    return await service.register_user(user_in)

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service)
):
    """
    Prijava korisnika i generiranje JWT tokena.
    OAuth2PasswordRequestForm očekuje 'username' (što je kod tebe email) i 'password'.
    """
    return await service.login_user(form_data.username, form_data.password)
@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Vraća podatke trenutno prijavljenog korisnika.
    Ispunjava uvjet: Endpoint /auth/me koji vraća trenutnog korisnika.
    """
    return current_user