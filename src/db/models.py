from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.db.database import Base

# to make table
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)