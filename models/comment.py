from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(String, primary_key=True, index=True)
    issue_id = Column(String, ForeignKey("issues.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    issue = relationship("Issue", back_populates="comments")
    user = relationship("User", back_populates="comments")
