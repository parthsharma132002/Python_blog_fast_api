from sqlalchemy.orm import Session
from src.blog import module, schema

def create_blog(db: Session, blog: schema.BlogCreate):
    db_blog = module.Blog(title=blog.title, content=blog.content)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog(db: Session, blog_id: int):
    return db.query(module.Blog).filter(module.Blog.id == blog_id).first()

def get_blogs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(module.Blog).offset(skip).limit(limit).all()
