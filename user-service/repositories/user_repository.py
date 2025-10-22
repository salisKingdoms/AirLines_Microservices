import asyncpg
from passlib.context import CryptContext
from models.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def create_user(self, user: UserCreate) -> str:
        # Check if email/username exists
        exists = await self.conn.fetchval(
            "SELECT 1 FROM users WHERE email = $1 OR username = $2",
            user.email, user.username
        )
        if exists:
            raise ValueError("Email or username already registered")

        hashed_pw = pwd_context.hash(user.password)
        user_id = await self.conn.fetchval(
            """
            INSERT INTO users (email, username, password_hash, first_name, last_name)
            VALUES ($1, $2, $3, $4, $5) RETURNING id
            """,
            user.email, user.username, hashed_pw, user.first_name, user.last_name
        )
        return str(user_id)

    async def get_user_by_email(self, email: str):
        row = await self.conn.fetchrow(
            """
        SELECT 
            id, email, username, first_name, last_name, phone,
            is_active, is_verified, password_hash,
            created_at, updated_at, last_login_at,
            failed_login_attempts, locked_until
        FROM users 
        WHERE email = $1
        """,
            email
        )
        if row:
            # Konversi UUID ke string
            return {
                "id": str(row["id"]),
                "email": row["email"],
                "username": row["username"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "phone": row["phone"],
                "is_active": row["is_active"],
                "is_verified": row["is_verified"],
                "password_hash": row["password_hash"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "last_login_at": row["last_login_at"],
                "failed_login_attempts": row["failed_login_attempts"],
                "locked_until": row["locked_until"],
            }
        return None