from fastapi import FastAPI
# Provjeri putanju: mapa routers, pa datoteka user_router
from routers.user_router import router as user_router

app = FastAPI(title="Zadarsko Ludilo Gym")

app.include_router(user_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Sustav Zadarsko Ludilo Gym je pokrenut!"}