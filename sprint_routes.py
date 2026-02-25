from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/sprints")

@router.post("/", response_model=schemas.Sprint)
def create_sprint(
    sprint_create: schemas.SprintCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Validate date range
    if sprint_create.end_date <= sprint_create.start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    
    # Check for duplicate sprint name
    existing_sprint = db.query(models.Sprint).filter(
        models.Sprint.name == sprint_create.name,
        models.Sprint.owner_id == current_user.id
    ).first()
    
    if existing_sprint:
        raise HTTPException(status_code=400, detail="Sprint name must be unique")
    
    sprint = models.Sprint(
        name=sprint_create.name,
        start_date=sprint_create.start_date,
        end_date=sprint_create.end_date,
        owner_id=current_user.id
    )
    
    db.add(sprint)
    db.commit()
    db.refresh(sprint)
    return sprint

@router.get("/{sprint_id}", response_model=schemas.SprintWithIssues)
def get_sprint(
    sprint_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    # Ensure user has access to the sprint
    if sprint.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this sprint")
    
    # Get all issues in this sprint
    issues = db.query(models.Issue).filter(models.Issue.sprint_id == sprint_id).all()
    
    return {
        "id": sprint.id,
        "name": sprint.name,
        "start_date": sprint.start_date,
        "end_date": sprint.end_date,
        "owner_id": sprint.owner_id,
        "issues": issues
    }

@router.patch("/{issue_id}/sprint", response_model=schemas.Issue)
def assign_issue_to_sprint(
    issue_id: int,
    sprint_assign: schemas.SprintAssign,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    issue = db.query(models.Issue).filter(models.Issue.id == issue_id).first()
    
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Ensure user has access to the issue
    if issue.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this issue")
    
    # Validate sprint exists
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_assign.sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    # Update issue with new sprint
    issue.sprint_id = sprint_assign.sprint_id
    db.commit()
    db.refresh(issue)
    return issue
