from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SprintCreate(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    
    class Config:
        orm_mode = True

class SprintAssign(BaseModel):
    sprint_id: int
    
    class Config:
        orm_mode = True

class SprintWithIssues(BaseModel):
    id: int
    name: str
    start_date: datetime
    end_date: datetime
    owner_id: int
    issues: list
    
    class Config:
        orm_mode = True
