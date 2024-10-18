import json
import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from app.infrastructure.database.models.users import User
from app.infrastructure.database.repo.requests import RequestsRepo
from app.webhook.auth import get_twa_user
from app.webhook.utils import get_repo

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/questions")
async def get_questions(
    request: Request,
    repo: RequestsRepo = Depends(get_repo),
    user: User = Depends(get_twa_user),
):
    # Fetch 10 random questions from the database
    questions = await repo.questions.get_random_questions(limit=10)

    # Convert questions to the desired format
    formatted_questions = [
        {
            "id": question.id,
            "text": question.text,
            "emoji": question.emoji,
            "answers": [
                {"user_id": 13, "user_name": "gennady", "answer_text": "Геннадий"},
                {"user_id": 14, "user_name": "andrey", "answer_text": "Андрей"},
                {"user_id": 15, "user_name": "alexander", "answer_text": "Александр"},
                {"user_id": 16, "user_name": "petr", "answer_text": "Петр"},
            ],
        }
        for question in questions
    ]

    return formatted_questions


@router.get("/profile")
async def get_profile(
    request: Request,
    repo: RequestsRepo = Depends(get_repo),
    user: User = Depends(get_twa_user),
):
    # Create a profile object using the TelegramUser data
    profile = {
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
        "photo_url": user.photo_url,
    }

    print(f"Returning profile for user: {user.user_id}")
    return profile


@router.get("/friends")
async def get_friends(
    request: Request,
    repo: RequestsRepo = Depends(get_repo),
    user: User = Depends(get_twa_user),
):
    friends = await repo.users.get_friends(user.user_id)
    logger.info(f"Returning friends for user: {user.user_id}, friends: {friends}")
    return friends


@router.post("/add_friend")
async def add_friend(
    request: Request,
    repo: RequestsRepo = Depends(get_repo),
    user: User = Depends(get_twa_user),
):
    request_data = await request.json()
    logger.info(f"Request data: {request_data}")
    friend_id = request_data.get("friend_id")
    logger.info(f"{friend_id} of type {type(friend_id)}")
    friend = await repo.users.get_user_by_id(friend_id)
    await repo.users.add_friend(user.user_id, friend.user_id)
    logger.info(f"User {user.user_id} added friend {friend.user_id}")
    return {"status": "success"}
