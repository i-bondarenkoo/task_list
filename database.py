from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from pathlib import Path

BASE_DIR = Path(__file__).parent

engine = create_async_engine(
    "postgresql+asyncpg://postgres:123456@localhost:5433/task", echo=True
)


AsyncSession = async_sessionmaker(bind=engine)


# функция для получения сесcии
async def get_session():
    async with AsyncSession() as session:
        yield session


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    # access_token_exp_minutes: int = 3
    access_token_exp_minutes: int = 15


auth_jwt = AuthJWT()
