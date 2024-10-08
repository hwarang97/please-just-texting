from app.models.base import User
from app.schemas import DeleteModel
from app.schemas import PasswordModel
from app.schemas import UserCreateModel
from app.schemas import UserModel
from app.schemas import UserSigninModel
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import and_
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_name(db: AsyncSession, name: str) -> User | None:
    statement = select(User).where(name == User.name)
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    statement = select(User).where(email == User.email)
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def check_user_exists(db: AsyncSession, user: UserSigninModel) -> None:
    db_user: str | None = await get_user_by_name(db=db, name=user.name)
    if db_user and pwd_context.verify(user.password, db_user.password_hash):
        return
    raise HTTPException(status_code=401, detail="Invalid username or password")


async def check_user_duplicate(db: AsyncSession, name: str, email: str) -> None:
    existing_user_by_name: str | None = await get_user_by_name(db=db, name=name)
    existing_user_by_email: str | None = await get_user_by_email(db=db, email=email)
    if existing_user_by_name or existing_user_by_email:
        raise HTTPException(status_code=400, detail="username or email already exits")


async def create_user(db: AsyncSession, user: UserCreateModel) -> UserModel:
    await check_user_duplicate(name=user.name, email=user.email, db=db)
    password_hash = pwd_context.hash(user.password)
    db_user = User(name=user.name, password_hash=password_hash, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    user_model = UserModel.model_validate(db_user)
    return user_model


async def update_user(db: AsyncSession, user: PasswordModel) -> None:
    statement = select(User).where(and_(User.name == user.name, User.email == user.email))
    result = await db.execute(statement)
    db_user = result.scalar()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid username or email")
    hashed_password = pwd_context.hash(user.new_password)
    db_user.password_hash = hashed_password
    await db.commit()


async def delete_user(db: AsyncSession, user: DeleteModel) -> None:
    statement = delete(User).where(and_(User.name == user.name, User.email == user.email))
    user_signin = UserSigninModel(name=user.name, password=user.password)
    await check_user_exists(user=user_signin, db=db)
    await db.execute(statement)
    await db.commit()
