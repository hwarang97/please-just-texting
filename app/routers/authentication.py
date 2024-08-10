from app.dependencies import session
from app.models.dao.users import check_user_exists
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(default_response_class=JSONResponse, tags=["token"])


@router.post("/token")
async def singin(form_data: OAuth2PasswordRequestFormStrict = Depends(), db: AsyncSession = Depends(session)):
    await check_user_exists(name=form_data.username, db=db)
    return {"access_token": "asdf", "token_type": "bearer"}
