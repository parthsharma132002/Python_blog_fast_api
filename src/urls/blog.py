from fastapi import APIRouter,Depends, Request
from sqlalchemy.orm import Session
#Local Imports
from src.blog.serializer import (BlogCreateSerializer, BlogRequestSerializer, BlogResponseSerializer, BlogUpdateSerializer)
from src.blog.controller import BlogModule

router = APIRouter(prefix="/blog")

"""Blog add,get,update,delete"""

@router.post("/create")
@router.post("/create/")
async def create_blog(request:BlogCreateSerializer):
    return await BlogModule.create_blog(request=request)

@router.get("/blog_get")
@router.get("/blog_get/")
async def get_blogs():
    return await BlogModule.get_blogs()

@router.get("/blog_get_pk/{id}")
@router.get("/blog_get_pk/{id}/")
async def get_blog_by_id( id:int):
    return await BlogModule.get_blog_by_id(id=id)

@router.put("/blog_update_pk/{id}")
@router.put("/blog_update_pk/{id}/")
async def update_blog_by_id(request:BlogUpdateSerializer, id:int):
    return await BlogModule.update_blog_by_id(request=request, id=id)

@router.delete("/blog/{id}")
@router.delete("/blog/{id}/")
async def delete_blog(id:int):
    return await BlogModule.delete_blog(id=id)
