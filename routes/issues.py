from fastapi import APIRouter, HTTPException, Path
from typing import Optional
from models.issue import Issue
from utils.status_transitions import ALLOWED_TRANSITIONS, Status, Transition
from database import get_issue_by_id, update_issue_status

router = APIRouter()

@router.patch("/issues/{issue_id}/status")
async def update_issue_status(issue_id: str, new_status: str):
    issue = get_issue_by_id(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    current_status = issue.status
    if new_status not in Status._value2member_map_:
        raise HTTPException(status_code=400, detail="Invalid status")

    allowed_transitions = ALLOWED_TRANSITIONS.get(current_status, [])
    if new_status not in [Transition(value).name for value in allowed_transitions]:
        raise HTTPException(status_code=400, detail="Invalid transition")

    update_issue_status(issue_id, new_status)
    return {"message": "Status updated successfully"}
