import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT") 

    print(f"DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}, DB_NAME: {DB_NAME}, DB_HOST: {DB_HOST}, DB_PORT: {DB_PORT}")

    # Database connection URL
    DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    