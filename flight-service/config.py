import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/airline_flight")
SECRET_KEY = os.getenv("SECRET_KEY", "f4c59e9b1e008d29692e04c2a8e8adfa933186be986bf04bde5792236e858de6")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30