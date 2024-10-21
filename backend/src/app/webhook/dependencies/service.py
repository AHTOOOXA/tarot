from fastapi import Depends

from app.infrastructure.database.repo.requests import RequestsRepo
from app.services.requests import RequestsService
from app.webhook.dependencies.database import get_repo


async def get_services(repo: RequestsRepo = Depends(get_repo)):
    yield RequestsService(repo)
