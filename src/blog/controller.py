from fastapi import status, UploadFile, HTTPException
from typing import Optional, List
from pydantic import UUID4
import logging
import uuid
from src.blog.schema import BlogSchema
from src.blog.serializer import (
    BlogPostRequestSerializer,
    BlogPostResponseSerializer,
    SuccessResponseSerializer,
    ErrorResponseSerializer,
)
from src.utils.constant import BlogMessages

class BlogController:

    @classmethod
    async def create_blog_post(
        cls, 
        request: BlogPostRequestSerializer, 
    ):
        created_post = await BlogSchema.create_blog_post(
            request = request, 
        )
        if not created_post:
            logging.error(BlogMessages.FAILED_CREATE)
            serializer = ErrorResponseSerializer(
                status_code = status.HTTP_400_BAD_REQUEST,
                message = BlogMessages.FAILED_CREATE,
                data = {},
            )
        else:
            logging.info(BlogMessages.CREATED_SUCCESS)
            serializer = SuccessResponseSerializer(
                status_code = status.HTTP_200_OK,
                message = BlogMessages.CREATED_SUCCESS,
                data=BlogPostResponseSerializer(**created_post.__dict__).dict()
            )
        return serializer

    @classmethod
    async def get_all_blog_posts(
        cls, 
        page,
        limit,
        search_text: Optional[str] = None
    ):
        posts = await BlogSchema.get_all_blog_posts(
            page = page,
            limit = limit, 
            search_text = search_text
        )
        serialized_posts = [
            BlogPostResponseSerializer.model_validate(post.__dict__) for post in posts
        ]
        serializer = SuccessResponseSerializer(
            status_code = status.HTTP_200_OK,
            message = BlogMessages.FETCH_ALL_SUCCESS,
            data = serialized_posts,
        )
        return serializer

    @classmethod
    async def get_blog_post(
        cls, 
        blog_id: UUID4
    ):
        post = await BlogSchema.get_blog_post(
            blog_id
        )
        if not post:
            return ErrorResponseSerializer(
                status_code = status.HTTP_400_BAD_REQUEST,
                message = BlogMessages.NOT_FOUND,
                data = {},
            )
        return SuccessResponseSerializer(
            status_code = status.HTTP_200_OK,
            message = BlogMessages.FETCHED_SUCCESS,
            data = BlogPostResponseSerializer(**post.__dict__).dict()
        )

    @classmethod
    async def update_blog_post(cls, blog_id: UUID4, request: BlogPostRequestSerializer):
        updated_post = await BlogSchema.update_blog_post(
            blog_id, 
            request
        )
        if not updated_post:
            return ErrorResponseSerializer(
                status_code = status.HTTP_400_BAD_REQUEST,
                message = BlogMessages.FAILED_UPDATED,
                data = {},
            )
        return SuccessResponseSerializer(
            status_code = status.HTTP_200_OK,
            message = BlogMessages.UPDATED_SUCCESS,
            data = BlogPostResponseSerializer(**updated_post.__dict__).dict()
        )

    @classmethod
    async def delete_blog_post(
        cls, 
        blog_id: UUID4
    ):
        success = await BlogSchema.delete_blog_post(
            blog_id
        )
        if not success:
            return ErrorResponseSerializer(
                status_code = status.HTTP_400_BAD_REQUEST,
                message = BlogMessages.FAILED_DELETED,
                data = {},
            )
        return SuccessResponseSerializer(
            status_code = status.HTTP_200_OK,
            message = BlogMessages.DELETED_SUCCESS,
            data = {},
        )
