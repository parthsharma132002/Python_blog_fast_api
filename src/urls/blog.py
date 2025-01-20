from fastapi import APIRouter, HTTPException, status
from pydantic import UUID4
from src.blog.controller import BlogController
from src.blog.serializer import BlogPostRequestSerializer, SuccessResponseSerializer


router = APIRouter(prefix = "/blog")

@router.post("/blogs")
async def create_blog_post(
    request: BlogPostRequestSerializer
):
    return await BlogController.create_blog_post(
        request = request
    )

@router.get("/blogs")
async def get_all_blog_posts(
    page: int = 1,
    limit: int = 10,
    search_text: str = None,
):
    return await BlogController.get_all_blog_posts(
        page = page,
        limit = limit,
        search_text = search_text
    )

@router.get("/blogs/{blog_id}")
async def get_blog_post(
    blog_id: UUID4
):
    return await BlogController.get_blog_post(
        blog_id = blog_id
    )

@router.put("/blogs/{blog_id}")
async def update_blog_post(
    blog_id: UUID4, 
    request: BlogPostRequestSerializer
):
    return await BlogController.update_blog_post(
        blog_id = blog_id, 
        request = request
    )

@router.delete("/blogs/{blog_id}")
async def delete_blog_post(
    blog_id: UUID4
):
    return await BlogController.delete_blog_post(
        blog_id = blog_id
    )



