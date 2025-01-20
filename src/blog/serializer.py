from pydantic import BaseModel, UUID4, field_validator
from typing import Optional, List, Any
from datetime import datetime

# Request Serializer
class BlogPostRequestSerializer(BaseModel):
    title: str
    content: str
    thumbnail: Optional[str] = None 
    tags: Optional[List[str]] = []
    published: Optional[bool] = False

# Response Serializer
class BlogPostResponseSerializer(BaseModel):
    id: UUID4
    title: str
    content: str
    thumbnail: Optional[str] = None
    tags: List[str]
    published: bool
    created_at: datetime
    updated_at: datetime
        
    class Config:
        from_attributes = True

# Success and Error Response Serializers
class SuccessResponseSerializer(BaseModel):
    status_code: int
    message: str
    data: Any = None

class ErrorResponseSerializer(BaseModel):
    status_code: int
    message: str
    data: Any = None
