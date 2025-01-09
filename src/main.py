# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local Imports
from src.db import models  
from src.db.database import db
from src.urls import blog

def init_app():
    db.init()

    app = FastAPI(
        title="Blog API",
        description="A FastAPI Blog Application",
        version="1",
    )

    app.include_router(blog.router)

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = init_app()


@app.on_event("startup")
async def on_startup():
    await db.create_all()
