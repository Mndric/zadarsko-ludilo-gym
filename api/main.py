from fastapi import FastAPI
from routers.user_router import router as user_router
from routers.training_router import router as training_router


app = FastAPI(title="Zadarsko Ludilo Gym")

app.include_router(user_router, tags=["Authentication"])
app.include_router(training_router)

@app.get("/")
async def root():
    return {"message": "Dobrodošli u Zadarsko Ludilo Gym!"}