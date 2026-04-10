from fastapi import HTTPException, status
from repositories.user_repository import UserRepository
from core.security import hash_password, verify_password, create_access_token

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data):
        # Provjera postoji li već korisnik
        existing = await self.user_repo.get_by_email(user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Korisnik s ovim emailom već postoji"
            )
        
        hashed_pwd = hash_password(user_data.password)
        
        user_dict = {
            "email": user_data.email,
            "hashed_password": hashed_pwd,
            "is_admin": False  
        }
        
        return await self.user_repo.create(user_dict)

    async def login_user(self, email, password):
        user = await self.user_repo.get_by_email(email)
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Neispravan email ili lozinka"
            )
        
        access_token = create_access_token(
            data={"sub": user.email, "is_admin": user.is_admin}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }