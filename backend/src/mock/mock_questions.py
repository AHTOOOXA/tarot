import asyncio
import os
import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.repo.requests import RequestsRepo

# Initialize Faker
fake = Faker()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = "5452"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# List of emojis to choose from
emojis = ["😀", "😎", "🤔", "🧐", "💡", "🌟", "🔥", "🚀", "💻", "🌈"]

# Function to generate a mock question
def generate_mock_question():
    return {
        "text": fake.sentence(nb_words=10, variable_nb_words=True),
        "emoji": random.choice(emojis),
    }


# Function to add mock questions to the database
async def add_mock_questions(num_questions: int):
    async with async_session() as session:
        repo = RequestsRepo(session)
        for _ in range(num_questions):
            question_data = generate_mock_question()
            await repo.questions.create_question(**question_data)

        print(f"{num_questions} mock questions added to the database.")


# Main function to run the script
async def main():
    num_questions = 50  # Change this to the number of mock questions you want to generate
    await add_mock_questions(num_questions)


if __name__ == "__main__":
    asyncio.run(main())
