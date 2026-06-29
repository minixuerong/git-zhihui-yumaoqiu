from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import json

from .. import schemas
from .. import crud
from ..database import get_db
from .users import get_current_active_user

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])

@router.get("/jobs/{job_id}/cleaned")
def get_cleaned_job_data(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    capabilities = crud.get_capability_requirements(db, job_id=job_id)
    capability_list = []
    
    for cap in capabilities:
        skill = crud.get_skill(db, skill_id=cap.skill_id)
        capability_list.append({
            "skill_id": cap.skill_id,
            "skill_name": skill.name if skill else "",
            "requirement_type": cap.requirement_type.value,
            "level_required": cap.level_required.value if cap.level_required else "",
            "importance_score": cap.importance_score
        })
    
    return {
        "job_id": db_job.id,
        "job_name": db_job.name,
        "job_code": db_job.code,
        "department": db_job.department,
        "core_responsibilities": db_job.core_responsibilities,
        "typical_scenarios": db_job.typical_scenarios,
        "capabilities": capability_list,
        "confidence_score": db_job.confidence_score
    }

@router.post("/submit", response_model=schemas.AIAnalysisResultResponse,
             status_code=status.HTTP_201_CREATED)
def submit_analysis_result(result: schemas.AIAnalysisResultBase, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=result.job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return crud.create_ai_analysis_result(db, result=result)

@router.get("/results", response_model=list[schemas.AIAnalysisResultResponse])
def read_analysis_results(skip: int = 0, limit: int = 100, job_id: int = None,
                          db: Session = Depends(get_db),
                          current_user: schemas.UserResponse = Depends(get_current_active_user)):
    results = crud.get_ai_analysis_results(db, skip=skip, limit=limit, job_id=job_id)
    return results

@router.get("/results/{result_id}", response_model=schemas.AIAnalysisResultResponse)
def read_analysis_result(result_id: int, db: Session = Depends(get_db),
                         current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_result = crud.get_ai_analysis_result(db, result_id=result_id)
    if db_result is None:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    return db_result