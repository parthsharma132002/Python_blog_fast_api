from fastapi import FastAPI
from src.blog.controller import router as blog_router
from src.database import engine, Base
from urls.blog import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(blog_router)
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}
