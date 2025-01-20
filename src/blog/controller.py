from fastapi import status,HTTPException,Query
from src.db.database import db
from sqlalchemy import select,update
import sqlalchemy
#Local Imports
# from src.config.config import conf
from src.utils import constant,response
from src.utils.constant import BlogMessages
from src.utils.response import SuccessResponseSerializer,ErrorResponseSerializer
from src.blog.serializer import (
    BlogCreateSerializer, BlogRequestSerializer, BlogResponseSerializer, BlogUpdateSerializer
)
from src.blog.schema import (
    BlogSchema
)
from src.db.models import (
    Blog  
)

class BlogModule():

    @classmethod
    async def create_blog(cls, request:BlogCreateSerializer):
        if request:
            if request.title == "" or request.content == "":
                return response.ErrorResponseSerializer(message = constant.BlogMessages.PROPER_DATA_ERROR)
            else:
                context = {
                    'message':constant.BlogMessages.CREATED_SUCCESS,
                    'status': status.HTTP_200_OK,
                    'data':await BlogSchema.create_blog(request=request)
                }
                return context
        else:
            return response.ErrorResponseSerializer(message = constant.BlogMessages.REQUEST_ERROR)    
        
    @classmethod
    async def get_blogs(cls):
        context = {
                'message':constant.BlogMessages.FETCH_ALL_SUCCESS,
                'status':status.HTTP_200_OK,
                'data':await BlogSchema.get_all_blog()
            }
        return context
    
    @classmethod
    async def get_blog_by_id(cls, id):
        try:
            context = {
                'message':constant.BlogMessages.FETCHED_SUCCESS,
                'status':status.HTTP_200_OK,
                'data':await BlogSchema.get_blog(id=id)
            }    
            return context
        except Exception as e:
            return response.ErrorResponseSerializer(message = constant.BlogMessages.ID_ERROR+f" {e}")
        
    @classmethod
    async def update_blog_by_id(cls, request:BlogUpdateSerializer, id):
        try:

            if request:
                if request.title == "" and request.content == "":
                    return response.ErrorResponseSerializer(message = constant.BlogMessages.PROPER_DATA_ERROR)
                updated_blog = await BlogSchema.update_blog(request=request, id=id)
        
                if updated_blog == constant.BlogMessages.NOT_FOUND:
                    return response.ErrorResponseSerializer(message=constant.BlogMessages.NOT_FOUND)
                else:
                    context = {
                            'message':constant.BlogMessages.UPDATED_SUCCESS,
                            'status':status.HTTP_200_OK,
                            'data':await BlogSchema.update_blog(request=request, id=id)
                        }
                    return context
            else:
                return response.ErrorResponseSerializer(message = constant.BlogMessages.REQUEST_ERROR)
        except Exception as e:
            return response.ErrorResponseSerializer(message = constant.BlogMessages.ID_ERROR+f" {e}")

    @classmethod
    async def delete_blog(cls, id):
        try:
            deleted = await BlogSchema.delete_blog_id(id=id)
            if deleted is None:
                context = {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': constant.BlogMessages.NOT_FOUND,
                    'data': None
                }
            else: 
                context = {
                    'status': status.HTTP_200_OK,
                    'message': constant.BlogMessages.DELETED_SUCCESS,
                    'data': True
                }
            return context
        except Exception as e:
            return response.ErrorResponseSerializer(message=constant.BlogMessages.ID_ERROR + f" {e}")


