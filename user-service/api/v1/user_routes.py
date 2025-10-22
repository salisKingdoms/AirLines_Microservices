from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from repositories.user_repository import UserRepository
from services.user_service import UserService
from models.user import UserCreate, UserLogin
from security.auth import create_access_token

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/register")
async def register(user: UserCreate, conn=Depends(get_db)):
    try:
        repo = UserRepository(conn)
        service = UserService(repo)
        user_id = await service.register_user(user)
        return {"message": "User created", "user_id": str(user_id)}  # pastikan string
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("🔥 Critical error:", repr(e))  # lihat di terminal
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login")
async def login(form: UserLogin, conn=Depends(get_db)):
    repo = UserRepository(conn)
    service = UserService(repo)
    user = await service.authenticate_user(form.email, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user['id'])})
    return {"access_token": token, "token_type": "bearer"}