from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import sessionLocal
from src.blog import schema, serializer

router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# to create data
@router.post("/blogs/", response_model=schema.Blog)
async def create_blog(blog: schema.BlogCreate, db: Session = Depends(get_db)):
    return serializer.create_blog(db=db, blog=blog)

# to get specific data
@router.get("/blogs/{blog_id}", response_model=schema.Blog)
async def read_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = serializer.get_blog(db=db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return db_blog

#  to get list of data 
@router.get("/blogs/", response_model=list[schema.Blog])
async def read_blogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return serializer.get_blogs(db=db, skip=skip, limit=limit)


@router.put("/blogs/{blog_id}", response_model=schema.Blog)
async def update_blog(blog_id: int, blog: schema.BlogCreate, db: Session = Depends(get_db)):
    db_blog = serializer.get_blog(db=db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Used for Update the blog
    db_blog.title = blog.title
    db_blog.content = blog.content
    db.commit()
    db.refresh(db_blog)
    return db_blog

# to delete data
@router.delete("/blogs/{blog_id}", response_model=schema.Blog)
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = serializer.get_blog(db=db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(db_blog)
    db.commit()
    return db_blog