from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Comment, Issue
from app.schemas import CommentCreate, CommentResponse
from app.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/issues/{issue_id}", status_code=status.HTTP_201_CREATED)
async def create_comment(
    issue_id: str,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Check if issue exists
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not db_issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    
    # Create new comment
    new_comment = Comment(
        issue_id=issue_id,
        user_id=current_user["id"],
        content=comment.content
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return CommentResponse.from_orm(new_comment)

@router.get("/issues/{issue_id}")
async def get_issue_with_comments(
    issue_id: str,
    db: Session = Depends(get_db)
):
    # Get issue with comments
    db_issue = db.query(Issue).options(db.joinedload(Issue.comments)).filter(Issue.id == issue_id).first()
    
    if not db_issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    
    return db_issue
