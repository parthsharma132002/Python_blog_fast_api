from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from src.config.database import Base

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    thumbnail = Column(String, nullable=True)
    tags = Column(JSON, nullable=True, default=[])
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
