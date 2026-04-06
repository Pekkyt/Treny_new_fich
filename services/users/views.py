from fastapi import APIRouter, Depends, HTTPException, status
from core.auth import create_access_token
from .schemas import UserCreate, UserRead, Token
from core.models.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .dependencies import get_current_user
from core.models.user import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["USERS"], prefix="/users")


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_dependencies)
):
    return await crud.create_user(user_in=user_in, session=session)


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.session_dependencies),
):
    user = await crud.authenticate_user(
        session=session, email=form_data.username, password=form_data.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user
