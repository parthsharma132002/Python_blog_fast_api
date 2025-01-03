from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.blog.controller import get_db
from src.blog import schema, serializer
from src.blog import controller

router = APIRouter()

@router.post("/blogs/", response_model=serializer.Blog)
async def create_blog(blog: serializer.BlogCreate, db: Session = Depends(get_db)):
    return await controller.create_blog(blog=blog,db=db)

@router.get("/blogs/{blog_id}", response_model=serializer.Blog)
async def read_blog_route(blog_id: int, db: Session = Depends(get_db)):
    return await controller.get_blog_by_id(blog_id, db)

@router.get("/blogs/", response_model=list[serializer.Blog])
async def read_blogs_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    blogs = await controller.get_blogs(skip=skip, limit=limit, db=db)
    return blogs 

@router.put("/blogs/{blog_id}", response_model=serializer.Blog)
async def update_blog_route(blog_id: int, blog: serializer.BlogCreate, db: Session = Depends(get_db)):
    return await controller.update_blog(blog_id=blog_id, blog=blog, db=db)

@router.delete("/blogs/{blog_id}", response_model=serializer.Blog)
async def delete_blog_route(blog_id: int, db: Session = Depends(get_db)):
    return await controller.delete_blog(blog_id=blog_id, db=db)
