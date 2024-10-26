import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from app.schemas.inbox import InboxSchema
from app.schemas.quizzes import QuizResponseSchema, QuizSchema
from app.schemas.users import UpdateUserRequest, UserSchema
from app.services.requests import RequestsService
from app.webhook.auth import get_twa_user
from app.webhook.dependencies.service import get_services

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/inbox")
async def get_inbox(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
) -> InboxSchema:
    inbox = await services.inbox.get_inbox_messages(user.user_id)
    return inbox


@router.get("/quizzes")
async def get_quizzes(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
) -> List[QuizSchema]:
    quizzes = await services.quizzes.get_random_quizzes(user.user_id, limit=10)
    return quizzes


@router.post("/quiz_response")
async def post_quiz_response(
    quiz_response: QuizResponseSchema,
    services: RequestsService = Depends(get_services),
    user: UserSchema = Depends(get_twa_user),
):
    quiz_response.taker_id = user.user_id
    await services.quizzes.create_quiz_response(quiz_response)
    return {"status": "success"}


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
    await services.users.add_friend(user.user_id, friend_id)
    logger.info(f"User {user.user_id} added friend {friend_id}")
    return {"status": "success"}


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
):
    await services.users.update_user(user.user_id, user_data.dict())
    return {"status": "success"}
