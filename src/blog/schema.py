from sqlalchemy.future import select
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import UUID4
import logging
from src.blog.model import BlogPost 
from src.config.database import db  
from datetime import datetime
from src.utils.constant import BlogMessages

class BlogSchema:

    @classmethod
    async def create_blog_post(
        cls,
        request
    ):
        new_post = BlogPost(
            title = request.title,
            content = request.content,
            thumbnail = request.thumbnail,
            tags = request.tags,
            published = request.published,
        )
        db.add(new_post)
        try:
            await db.commit()
            logging.info(BlogMessages.CREATED_SUCCESS)
            return new_post
        except Exception as e:
            await db.rollback()
            logging.error(f"Error creating blog post: {e}")
            return None

    @classmethod
    async def get_all_blog_posts(
        cls,
        page: int,
        limit: int,
        search_text: Optional[str] = None,
    ) -> List[BlogPost]:
        try:
            query = select(
                BlogPost
            )
            if search_text:
                query = query.filter(
                    BlogPost.title.ilike(f"%{search_text}%")
                )
            
            result = await db.execute(query.offset((page - 1) * limit).limit(limit))
            posts = result.scalars().all()
            logging.info(BlogMessages.FETCH_ALL_SUCCESS)

            return posts
        except Exception as e:
            logging.error(f"Error fetching blog posts: {e}")
            return []
        
    @classmethod
    async def get_blog_post(
        cls, 
        blog_id: UUID4
    ) -> Optional[BlogPost]:
        try:
            query = select(
                BlogPost
            ).where(
                BlogPost.id == blog_id
            )
            result = await db.execute(query)
            post = result.scalar_one_or_none()
            logging.info(BlogMessages.FETCHED_SUCCESS)
            return post
        except Exception as e:
            logging.error(f"Error fetching blog post: {e}")
            return None

    @classmethod
    async def update_blog_post(
        cls, 
        blog_id: UUID4, 
        request
    ):
        try:
            post = await cls.get_blog_post(
                blog_id
            )
            if not post:
                return None
            post.title = request.title
            post.content = request.content
            post.thumbnail = request.thumbnail
            post.tags = request.tags
            post.published = request.published
            post.updated_at = datetime.utcnow()
            await db.commit()
            logging.info(BlogMessages.UPDATED_SUCCESS)
            return post
        except Exception as e:
            await db.rollback()
            logging.error(f"Error updating blog post: {e}")
            return None

    @classmethod
    async def delete_blog_post(
        cls, 
        blog_id: UUID4
    ) -> bool:
        try:
            post = await cls.get_blog_post(
                blog_id
            )
            if not post:
                return False
            await db.delete(post)
            await db.commit()
            logging.info(BlogMessages.DELETED_SUCCESS)
            return True
        except Exception as e:
            await db.rollback()
            logging.error(f"Error deleting blog post: {e}")
            return False