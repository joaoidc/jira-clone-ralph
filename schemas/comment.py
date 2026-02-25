from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: str
    content: str
    created_at: datetime
    user_id: str
    
    class Config:
        orm_mode = True
