from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user import User
from sqlalchemy.engine import Result
from core.auth import hash_password, verify_password
from .schemas import UserCreate
from sqlalchemy import select


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> User | None:
    user = await get_user_by_email(
        session=session,
        email=email,
    )
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user
