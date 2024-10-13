import json
import logging
from contextlib import suppress

import sqlalchemy.exc
from aiogram.utils.markdown import hbold, hcode
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from app.infrastructure.database.repo.requests import RequestsRepo
from app.webhook.auth import TelegramUser, get_twa_user
from app.webhook.utils import get_repo

router = APIRouter()


@router.get("/questions")
async def get_questions(
    request: Request,
    repo: RequestsRepo = Depends(get_repo),
    user: TelegramUser = Depends(get_twa_user),
):
    # Fetch 10 random questions from the database
    questions = await repo.questions.get_random_questions(limit=10)

    # Convert questions to the desired format
    formatted_questions = [
        {
            "question_id": question.id,
            "question_text": question.text,
            "question_emoji": question.emoji,
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
    user: TelegramUser = Depends(get_twa_user),
):
    # Create a profile object using the TelegramUser data
    profile = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
        "photo_url": user.photo_url,
    }

    print(f"Returning profile for user: {user.id}")
    return profile
