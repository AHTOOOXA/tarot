import json
import logging
from contextlib import suppress

import sqlalchemy.exc
from aiogram.utils.markdown import hbold, hcode
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from app.infrastructure.database.repo.requests import RequestsRepo
from app.webhook.utils import (bot, get_repo, parse_init_data,
                               validate_telegram_data)

router = APIRouter()


@router.post("/health")
async def book_slot(request: Request, repo: RequestsRepo = Depends(get_repo)):
    return {"status": "ok"}


@router.post("/repo_health")
async def book_slot(request: Request, repo: RequestsRepo = Depends(get_repo)):
    data = await request.json()

    init_data = data.get("userInitData")
    if init_data and not validate_telegram_data(init_data):
        raise HTTPException(status_code=400, detail="Invalid initData")

    parsed_data = parse_init_data(init_data)
    user = parsed_data.get("user")
    return {"user": user}

@router.get("/questions")
async def get_questions(request: Request, repo: RequestsRepo = Depends(get_repo)):
    # questions = await repo.get_questions()
    # return {"questions": questions} 

    # return mock json of questions
    return [
        {
            "question_id": 1,
            "question_text": "What is the capital of France?",
            "answers": [
                {"answer_text": "Paris", "is_correct": True},
                {"answer_text": "London", "is_correct": False},
                {"answer_text": "Berlin", "is_correct": False},
                {"answer_text": "Madrid", "is_correct": False}
            ]
        },
        {
            "question_id": 2,
            "question_text": "What is the capital of Germany?",
            "answers": [
                {"answer_text": "Paris", "is_correct": False},
                {"answer_text": "London", "is_correct": False},
                {"answer_text": "Berlin", "is_correct": True},
                {"answer_text": "Madrid", "is_correct": False}
            ]
        }
    ]
