import logging

from fastapi import APIRouter, FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from app.webhook import admin, routers
from app.webhook.dependencies.database import engine

app = FastAPI()

log_level = logging.INFO
log = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.getLogger(__name__).setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)


for router in [
    routers.base.router,
]:
    app.include_router(router)

app_admin = Admin(app, engine)

for view in [
    admin.users.UserAdmin,
    admin.questions.QuestionAdmin,
]:
    app_admin.add_view(view)
