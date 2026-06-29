from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import json

from .. import schemas
from .. import crud
from ..database import get_db
from .users import get_current_active_user

router = APIRouter(prefix="/api/v1/match", tags=["match"])

@router.post("/analysis", response_model=schemas.MatchAnalysisResponse)
def match_analysis(request: schemas.MatchAnalysisRequest, db: Session = Depends(get_db),
                   current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_resume = crud.get_resume(db, resume_id=request.resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    db_job = crud.get_job(db, job_id=request.job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    resume_skills = crud.get_resume_skills(db, resume_id=request.resume_id)
    job_requirements = crud.get_capability_requirements(db, job_id=request.job_id)
    
    resume_skill_dict = {rs.skill_id: rs.level for rs in resume_skills}
    job_skill_dict = {req.skill_id: (req.level_required, req.requirement_type) for req in job_requirements}
    
    matched_count = 0
    total_required = 0
    gaps = []
    
    level_order = {"beginner": 1, "intermediate": 2, "advanced": 3}
    
    for skill_id, (required_level, req_type) in job_skill_dict.items():
        if req_type == schemas.RequirementType.required:
            total_required += 1
            if skill_id in resume_skill_dict:
                resume_level = resume_skill_dict[skill_id]
                if level_order[resume_level] >= level_order[required_level]:
                    matched_count += 1
                else:
                    gaps.append({
                        "skill_id": skill_id,
                        "skill_name": crud.get_skill(db, skill_id=skill_id).name,
                        "current_level": resume_level,
                        "required_level": required_level,
                        "gap": level_order[required_level] - level_order[resume_level]
                    })
            else:
                gaps.append({
                    "skill_id": skill_id,
                    "skill_name": crud.get_skill(db, skill_id=skill_id).name,
                    "current_level": None,
                    "required_level": required_level,
                    "gap": "missing"
                })
    
    match_score = matched_count / total_required if total_required > 0 else 0.0
    
    improvement_suggestions = [
        f"提升技能 '{gap['skill_name']}' 从 {gap['current_level']} 到 {gap['required_level']}"
        for gap in gaps if gap.get("current_level")
    ] + [
        f"学习新技能 '{gap['skill_name']}'，要求等级: {gap['required_level']}"
        for gap in gaps if gap.get("current_level") is None
    ]
    
    learning_path = []
    for gap in gaps:
        skill_name = gap["skill_name"]
        level = gap["required_level"]
        learning_path.append(f"1. 学习 {skill_name} 基础")
        learning_path.append(f"2. 实践 {skill_name} 进阶")
        if level == "advanced":
            learning_path.append(f"3. 精通 {skill_name} 高级应用")
    
    gap_analysis_json = json.dumps(gaps, ensure_ascii=False)
    suggestions_json = json.dumps(improvement_suggestions, ensure_ascii=False)
    learning_path_json = json.dumps(learning_path, ensure_ascii=False)
    
    match_record = schemas.MatchRecordBase(
        resume_id=request.resume_id,
        job_id=request.job_id,
        match_score=match_score,
        gap_analysis=gap_analysis_json,
        improvement_suggestions=suggestions_json,
        learning_path=learning_path_json
    )
    crud.create_match_record(db, record=match_record)
    
    return {
        "match_score": match_score,
        "gap_analysis": gaps,
        "improvement_suggestions": improvement_suggestions,
        "learning_path": learning_path
    }

@router.get("/records", response_model=list[schemas.MatchRecordResponse])
def read_match_records(skip: int = 0, limit: int = 100, resume_id: int = None,
                       job_id: int = None, db: Session = Depends(get_db),
                       current_user: schemas.UserResponse = Depends(get_current_active_user)):
    records = crud.get_match_records(db, skip=skip, limit=limit,
                                     resume_id=resume_id, job_id=job_id)
    return records

@router.get("/records/{match_id}", response_model=schemas.MatchRecordResponse)
def read_match_record(match_id: int, db: Session = Depends(get_db),
                      current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_record = crud.get_match_record(db, match_id=match_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Match record not found")
    return db_record