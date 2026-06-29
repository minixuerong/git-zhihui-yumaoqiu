from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import schemas
from .. import crud
from ..database import get_db
from .users import get_current_active_user

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])

@router.get("/", response_model=schemas.PaginatedResponse)
def read_skills(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: str = None,
    keyword: str = None,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    skills = crud.get_skills(db, skip=skip, limit=limit, category=category, keyword=keyword)
    total = crud.get_skills_count(db, category=category, keyword=keyword)
    return {
        "items": [schemas.SkillResponse.model_validate(skill) for skill in skills],
        "total": total,
        "page": skip // limit + 1,
        "size": limit
    }

@router.get("/{skill_id}", response_model=schemas.SkillResponse)
def read_skill(skill_id: int, db: Session = Depends(get_db),
               current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_skill = crud.get_skill(db, skill_id=skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return schemas.SkillResponse.model_validate(db_skill)

@router.post("/", response_model=schemas.SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(skill: schemas.SkillBase, db: Session = Depends(get_db),
                 current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_skill = crud.get_skill_by_code(db, code=skill.code)
    if db_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill code already exists"
        )
    return schemas.SkillResponse.model_validate(crud.create_skill(db=db, skill=skill))

@router.put("/{skill_id}", response_model=schemas.SkillResponse)
def update_skill(skill_id: int, skill_update: schemas.SkillUpdate, db: Session = Depends(get_db),
                 current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_skill = crud.get_skill(db, skill_id=skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    if skill_update.code and skill_update.code != db_skill.code:
        existing = crud.get_skill_by_code(db, code=skill_update.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skill code already exists"
            )
    return schemas.SkillResponse.model_validate(crud.update_skill(db, skill_id=skill_id, skill_update=skill_update.model_dump(exclude_unset=True)))

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: int, db: Session = Depends(get_db),
                 current_user: schemas.UserResponse = Depends(get_current_active_user)):
    success = crud.delete_skill(db, skill_id=skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")