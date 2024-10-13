from sqladmin import ModelView

from app.infrastructure.database.models.questions import Question


class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.text, Question.emoji]
    column_searchable_list = [Question.text]
    column_sortable_list = [Question.id, Question.text]
