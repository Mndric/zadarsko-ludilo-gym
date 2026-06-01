from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_router import router as user_router
from routers.training_router import router as training_router


app = FastAPI(title="Zadarsko Ludilo Gym")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, tags=["Authentication"])
app.include_router(training_router)

@app.get("/")
async def root():
    return {"message": "Dobrodošli u Zadarsko Ludilo Gym!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)