from pydantic import BaseModel, constr
from typing import Optional


class BlogCreateSerializer(BaseModel):
    title: str
    content: str

class BlogRequestSerializer(BaseModel):
    id : int  

class BlogResponseSerializer(BaseModel):
    id : int
    title:Optional [str]
    content:Optional [str] 

class BlogUpdateSerializer(BaseModel):
    title:Optional [str]         
    content:Optional [str] 
