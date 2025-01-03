from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import sessionLocal
from src.blog import schema, serializer

from src.blog.model import Blog 

router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# get a blog by its ID
async def get_blog_by_id(blog_id: int, db: Session):
    db_blog = schema.get_blog(db=db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog

# create a new blog
async def create_blog(blog: serializer.BlogCreate, db: Session):
    return schema.create_blog(db=db, blog=blog)

# get all blogs 
async def get_blogs(skip: int, limit: int, db: Session):
    blogs = db.query(Blog).offset(skip).limit(limit).all() 
    return blogs

# update a blog
async def update_blog(blog_id: int, blog: serializer.BlogCreate, db: Session):
    db_blog = await get_blog_by_id(blog_id, db) 
    db_blog.title = blog.title
    db_blog.content = blog.content
    db.commit()
    db.refresh(db_blog)
    return db_blog

# delete a blog
async def delete_blog(blog_id: int, db: Session):
    db_blog = await get_blog_by_id(blog_id, db) 
    db.delete(db_blog)
    db.commit()
    return db_blog