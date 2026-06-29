from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from .. import schemas
from .. import crud
from ..database import get_db

router = APIRouter(prefix="/api/v1/crawler", tags=["crawler"])

@router.post("/submit", response_model=schemas.CrawlerSubmitResponse)
def submit_crawler_data(request: schemas.CrawlerSubmitRequest, db: Session = Depends(get_db)):
    created_count = 0
    updated_count = 0
    
    task_id = str(uuid4())
    crud.create_crawl_task(db, task=schemas.CrawlTaskBase(
        task_id=task_id,
        source_name="crawler"
    ))
    
    for job_data in request.jobs:
        existing_job = crud.get_job_by_code(db, code=job_data.code)
        if existing_job:
            update_data = job_data.dict(exclude_unset=True)
            crud.update_job(db, job_id=existing_job.id, job_update=schemas.JobUpdate(**update_data))
            updated_count += 1
        else:
            crud.create_job(db, job=job_data)
            created_count += 1
    
    crud.update_crawl_task_status(db, task_id=task_id, status="completed")
    
    return {
        "message": "Crawler data submitted successfully",
        "created_count": created_count,
        "updated_count": updated_count
    }
