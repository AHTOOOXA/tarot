import json
import logging
import random

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from app.infrastructure.database.models.users import User
from app.schemas.inbox import InboxSchema
from app.schemas.quizzes import QuizListSchema
from app.services.requests import RequestsService
from app.webhook.auth import get_twa_user
from app.webhook.dependencies.service import get_services

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/inbox")
async def get_inbox(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: User = Depends(get_twa_user),
) -> InboxSchema:
    inbox = await services.inbox.get_inbox_messages(user.user_id)
    return inbox


@router.get("/quizzes")
async def get_quizzes(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: User = Depends(get_twa_user),
) -> QuizListSchema:
    quizzes = await services.quizzes.get_random_quizzes(user.user_id, limit=10)
    return quizzes


@router.post("/quiz_response")
async def post_quiz_response(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: User = Depends(get_twa_user),
):
    request_data = await request.json()
    await services.quizzes.create_quiz_response(user.user_id, request_data)
    return {"status": "success"}


@router.get("/profile")
async def get_profile(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: User = Depends(get_twa_user),
):
    profile = await services.users.get_profile(user.user_id)
    print(f"Returning profile for user: {user.user_id}")
    return profile


@router.get("/friends")
async def get_friends(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: User = Depends(get_twa_user),
):
    friends = await services.users.get_friends(user.user_id)
    logger.info(f"Returning friends for user: {user.user_id}, friends: {friends}")
    return friends


@router.post("/add_friend")
async def add_friend(
    request: Request,
    services: RequestsService = Depends(get_services),
    user: User = Depends(get_twa_user),
):
    request_data = await request.json()
    logger.info(f"Request data: {request_data}")
    friend_id = request_data.get("friend_id")
    logger.info(f"{friend_id} of type {type(friend_id)}")
    await services.users.add_friend(user.user_id, friend_id)
    logger.info(f"User {user.user_id} added friend {friend_id}")
    return {"status": "success"}
