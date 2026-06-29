from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from .. import crud
from ..database import get_db

router = APIRouter(prefix="/api/v1/cleaner", tags=["cleaner"])


@router.post("/submit", response_model=schemas.CleanerSubmitResponse)
def submit_cleaned_data(request: schemas.CleanerSubmitRequest, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=request.job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    cleaned_data = request.cleaned_data
    
    # 从原始数据复制基础字段，用清洗结果覆盖
    new_job = schemas.JobCreate(
        name=cleaned_data.get("name") or db_job.name,
        code=db_job.code + "-cleaned",
        department=cleaned_data.get("department") or db_job.department,
        core_responsibilities=cleaned_data.get("core_responsibilities") or db_job.core_responsibilities,
        typical_scenarios=cleaned_data.get("typical_scenarios") or db_job.typical_scenarios,
        is_new=True,
        status=cleaned_data.get("status") or db_job.status,
        data_source=db_job.data_source,
        confidence_score=cleaned_data.get("confidence_score") or db_job.confidence_score,
        data_type="cleaned"
    )
    
    created_job = crud.create_job(db, job=new_job)
    
    return {
        "message": "Cleaned data submitted successfully",
        "job_id": created_job.id
    }