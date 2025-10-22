# user-service/main.py

from fastapi import FastAPI
from api.v1.user_routes import router as user_router  # ← correct import

app = FastAPI(
    title="Airline User Service",
    description="Handles user registration, login, and profile management.",
    version="1.0.0"
)

# Register the routes
app.include_router(user_router)  # ← this line is essential!
@app.get("/")
async def root():
    return {"service": "user-service", "status": "ok"}
    # return {
    #     "service": "user-service",
    #     "status": "running",
    #     "message": "Welcome to the Airline Ticketing System - User Service!"
    # }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected (to be implemented)"}

