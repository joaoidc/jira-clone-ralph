from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    key = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

    issues = relationship("Issue", back_populates="project")
