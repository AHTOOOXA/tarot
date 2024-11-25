import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from app.exceptions import FriendAlreadyExistsException, UserNotFoundException
from app.schemas.invites import InviteTokens
from app.schemas.start import StartData, StartParams
from app.schemas.users import UpdateUserRequest, UserSchema
from app.services.requests import RequestsService
from app.webhook.auth import get_twa_user
from app.webhook.dependencies.service import get_services

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/profile")
async def get_profile(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
):
    profile = await services.users.get_profile(user.user_id)
    print(f"Returning profile for user: {user.user_id}")
    return profile


@router.get("/friends")
async def get_friends(
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
) -> List[UserSchema]:
    friends = await services.users.get_friends(user.user_id)
    logger.info(f"Returning friends for user: {user.user_id}, friends: {friends}")
    return friends


@router.post("/add_friend")
async def add_friend(
    friend_id: int,
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
):
    try:
        await services.users.add_friend(user.user_id, friend_id)
        logger.info(f"User {user.user_id} added friend {friend_id}")
        return {"status": "success"}
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="Friend not found")
    except FriendAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Friend already exists")


@router.get("/user")
async def get_user(
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
) -> UserSchema:
    return user


@router.get("/user/{user_id}")
async def get_user_by_id(
    user_id: int,
    services: RequestsService = Depends(get_services),
) -> UserSchema:
    return await services.users.get_user_by_id(user_id)


@router.post("/user")
async def update_user(
    user_data: UpdateUserRequest,
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
) -> UserSchema:
    return await services.users.update_user(user.user_id, user_data)


@router.get("/invite_token", response_model=InviteTokens)
async def get_invite_token(
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
) -> InviteTokens:
    return await services.invites.create_invite(user.user_id)


@router.post("/process_start")
async def process_start(
    start_params: StartParams,
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
) -> StartData:
    print(f"Processing start with params: {start_params}")
    return await services.start.process_start(user, start_params)
