from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Sprint(Base):
    __tablename__ = "sprints"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="sprints")
    issues = relationship("Issue", back_populates="sprint")
    
    def __repr__(self):
        return f"<Sprint(id={self.id}, name='{self.name}')>"
