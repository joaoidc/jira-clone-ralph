from pydantic import BaseModel
from typing import Optional

class Issue(BaseModel):
    id: str
    title: str
    description: str
    status: str
    project_id: str

    class Config:
        schema_extra = {
            "example": {
                "id": "123",
                "title": "Bug in login",
                "description": "User can't login",
                "status": "Backlog",
                "project_id": "456"
            }
        }
