from fastapi import FastAPI
from api.v1.flight_routes import router as flight_router

app = FastAPI(title="Airline Flight Service", version="1.0")

app.include_router(flight_router)

@app.get("/")
async def root():
    return {"service": "flight-service", "status": "ok"}