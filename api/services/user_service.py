from fastapi import HTTPException
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data):
        existing = await self.user_repo.get_by_email(user_data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Korisnik već postoji")
        
        user_dict = {
            "email": user_data.email,
            "hashed_password": user_data.password 
        }
        return await self.user_repo.create(user_dict)