from sqladmin import ModelView

from app.infrastructure.database.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.user_id, User.username, User.full_name]
