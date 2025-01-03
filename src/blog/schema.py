from sqlalchemy.orm import Session
from src.blog import model, serializer

def create_blog(db: Session, blog: serializer.BlogCreate):
    db_blog = model.Blog(title=blog.title, content=blog.content)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog(db: Session, blog_id: int):
    return db.query(model.Blog).filter(model.Blog.id == blog_id).first()

def get_blogs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(model.Blog).offset(skip).limit(limit).all()
