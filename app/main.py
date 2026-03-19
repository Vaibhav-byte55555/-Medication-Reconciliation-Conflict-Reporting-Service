from fastapi import FastAPI
from app.routes.medication_routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Service running"}