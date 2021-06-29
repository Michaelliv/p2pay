from typing import List

from asyncpg import UniqueViolationError
from fastapi import APIRouter, HTTPException
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from common.logger import get_logger
from database.crud import users as user_crud
from common.models import User

logger = get_logger(__name__)

users_api_router = APIRouter()


@users_api_router.post("/users", status_code=201)
async def post_user(user: User):
    try:
        await user_crud.insert_user(user)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except UniqueViolationError:
        raise HTTPException(status_code=409, detail=f"User {user} already exists")


@users_api_router.get("/users", response_model=List[User])
async def get_users():
    return await user_crud.get_users()


@users_api_router.get("/users/{guid}/", response_model=User)
async def get_user_by_guid(guid: str):
    user = await user_crud.get_user_by_guid(guid=guid)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {guid} not found")
    return user
