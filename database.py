from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///task.db", echo=True)


AsyncSession = async_sessionmaker(bind=engine)


# функция для получения сесcии
async def get_session():
    async with AsyncSession() as session:
        yield session
