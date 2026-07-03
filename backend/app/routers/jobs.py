from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import schemas
from .. import crud
from ..database import get_db
from .users import get_current_active_user

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])

@router.get("/", response_model=schemas.PaginatedResponse)
def read_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category_id: int = None,
    status: str = None,
    keyword: str = None,
    new_only: bool = Query(False, description="仅显示今日新增岗位"),
    data_type: str = Query(None, description="数据类型: raw 或 cleaned"),
    uploader_id: int = Query(None, description="按发布者ID过滤"),
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    jobs = crud.get_jobs(db, skip=skip, limit=limit, category_id=category_id,
                         status=status, keyword=keyword, new_only=new_only,
                         data_type=data_type, uploader_id=uploader_id)
    total = crud.get_jobs_count(db, category_id=category_id, status=status,
                                 keyword=keyword, new_only=new_only,
                                 data_type=data_type, uploader_id=uploader_id)
    return {
        "items": [schemas.JobResponse.model_validate(job) for job in jobs],
        "total": total,
        "page": skip // limit + 1,
        "size": limit
    }

@router.get("/{job_id}", response_model=schemas.JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db),
             current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return schemas.JobResponse.model_validate(db_job)

@router.post("/", response_model=schemas.JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db),
               current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_job = crud.get_job_by_code(db, code=job.code)
    if db_job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job code already exists"
        )
    # 自动关联当前用户作为发布者
    job_data = job.model_dump()
    job_data["uploader_id"] = current_user.id
    # 招聘者发布的岗位自动标记为 cleaned（用户端可见）
    if current_user.role == 'hr':
        job_data["data_type"] = 'cleaned'
        if job_data.get("status") is None:
            job_data["status"] = 'active'
    return schemas.JobResponse.model_validate(crud.create_job(db=db, job=schemas.JobCreate(**job_data)))

@router.put("/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, job_update: schemas.JobUpdate, db: Session = Depends(get_db),
               current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_job = crud.update_job(db, job_id=job_id, job_update=job_update)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return schemas.JobResponse.model_validate(db_job)

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db),
               current_user: schemas.UserResponse = Depends(get_current_active_user)):
    success = crud.delete_job(db, job_id=job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")

@router.get("/{job_id}/capabilities", response_model=list[schemas.CapabilityRequirementResponse])
def get_job_capabilities(job_id: int, db: Session = Depends(get_db),
                         current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return [schemas.CapabilityRequirementResponse.model_validate(req) for req in crud.get_capability_requirements(db, job_id=job_id)]

@router.post("/{job_id}/capabilities", response_model=schemas.CapabilityRequirementResponse,
             status_code=status.HTTP_201_CREATED)
def add_job_capability(job_id: int, req: schemas.CapabilityRequirementBase,
                       db: Session = Depends(get_db),
                       current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db_skill = crud.get_skill(db, skill_id=req.skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return schemas.CapabilityRequirementResponse.model_validate(crud.create_capability_requirement(db, req=req, job_id=job_id))

@router.get("/{job_id}/evolutions", response_model=list[schemas.JobEvolutionResponse])
def get_job_evolutions(job_id: int, db: Session = Depends(get_db),
                       current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return [schemas.JobEvolutionResponse.model_validate(e) for e in crud.get_job_evolutions(db, job_id=job_id)]

@router.post("/{job_id}/evolutions", response_model=schemas.JobEvolutionResponse,
             status_code=status.HTTP_201_CREATED)
def create_job_evolution(job_id: int, evolution: schemas.JobEvolutionBase,
                         db: Session = Depends(get_db),
                         current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return schemas.JobEvolutionResponse.model_validate(crud.create_job_evolution(db, evolution=evolution, job_id=job_id))