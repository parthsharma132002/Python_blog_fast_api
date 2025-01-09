from sqlalchemy.orm import Session
from src.db.models import Blog
from src.db.database import db

from sqlalchemy.future import select
from sqlalchemy import update,delete,distinct,and_,or_
from src.utils import constant
from src.blog.serializer import (
    BlogCreateSerializer, BlogRequestSerializer, BlogResponseSerializer, BlogUpdateSerializer
)

class BlogSchema():

    @classmethod
    async def create_blog(cls, request:BlogCreateSerializer):
        blog_data = Blog(
            title = request.title,
            content = request.content,
        )
        try:    
            db.add(blog_data)
            try: 
                await db.commit()
            except Exception:
                await db.rollback()
            # return True     
            return blog_data
        except Exception as e:
            return e

    @classmethod
    async def get_blog(cls, id):
        blog_data = await db.execute(
            select(Blog)
            .where(Blog.id == id)
        )   

        if blog_data == None:
            return constant.BlogMessages.NOT_FOUND
        else: 
            blog_data = blog_data.scalars().one()
            data = {
                "id" : blog_data.id,
                "title" : blog_data.title,
                "content" : blog_data.content,
            }
            return data
        
    # @classmethod
    # async def get_all_blog(cls):
    #     blog_data = await db.execute(select(Blog))
    #     return blog_data.scalars().all()

    @classmethod
    async def get_all_blog(cls):
        result = await db.execute(select(Blog))
        blog_data_list = result.scalars().all()  
        data = [
            {
                "id": blog.id,
                "title": blog.title,
                "content": blog.content,
            }
            for blog in blog_data_list
        ]
        return data
    
        
    @classmethod
    async def update_blog(cls, request:BlogUpdateSerializer, id):
        blog_data = await db.execute(select(Blog).where(Blog.id == id))  
        if blog_data.scalars().one_or_none() == None:
            return constant.BlogMessages.NOT_FOUND
        else: 
            if request.title:
                blog_data = await db.execute(
                    update(Blog).where(Blog.id == id)
                    .values({"title": request.title})
                    .execution_options(synchronize_session="fetch")
                )
            if request.content:
                blog_data = await db.execute(
                    update(Blog).where(Blog.id == id)
                    .values({"content": request.content})
                    .execution_options(synchronize_session="fetch")
                )

            try:
                await db.commit()
            except Exception:
                await db.rollback()

            blog_data = await db.execute(select(Blog).where(Blog.id == id))       
            if blog_data == None:
                return constant.BlogMessages.NOT_FOUND
            else:
                return blog_data.scalars().one_or_none()

    @classmethod
    async def delete_blog_id(cls, id):
        query = delete(Blog).where(Blog.id == id)
        check_query = select(Blog).where(Blog.id == id) 
        try:
            existing_blog = await db.execute(check_query)
            if not existing_blog.scalar():  
                return None
            await db.execute(query)
            await db.commit()
            return True
        except Exception:
            await db.rollback()
