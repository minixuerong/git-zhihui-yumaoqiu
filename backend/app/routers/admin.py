from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import schemas
from .. import crud
from .. import models
from ..database import get_db
from .users import get_current_active_user, get_admin_user

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/dashboard/stats", response_model=schemas.DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    """获取数据概览统计：岗位数、技能数、用户数、待审核更新"""
    total_jobs = crud.get_jobs_count(db)
    total_skills = crud.get_skills_count(db)
    total_users = crud.get_users_count(db)
    pending_updates = db.query(models.JobEvolution).join(
        models.Job, models.JobEvolution.job_id == models.Job.id
    ).filter(
        models.Job.is_deleted == False
    ).count()
    today_new_jobs = crud.get_jobs_count(db, new_only=True)

    return {
        "total_jobs": total_jobs,
        "total_skills": total_skills,
        "total_users": total_users,
        "pending_updates": pending_updates,
        "today_new_jobs": today_new_jobs
    }


@router.get("/evolutions", response_model=list[schemas.EvolutionWithJobResponse])
def get_global_evolutions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    """获取全局演化记录（含岗位名称）"""
    evolutions = crud.get_all_evolutions(db, skip=skip, limit=limit)
    result = []
    for evo in evolutions:
        job_name = None
        if evo.job:
            job_name = evo.job.name
        result.append(schemas.EvolutionWithJobResponse(
            id=evo.id,
            job_id=evo.job_id,
            job_name=job_name,
            changes_summary=evo.changes_summary,
            changed_fields=evo.changed_fields,
            evolution_type=evo.evolution_type,
            created_at=evo.created_at
        ))
    return result


@router.get("/tasks", response_model=list[schemas.CrawlTaskResponse])
def get_task_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    """获取任务列表（爬取任务）"""
    return crud.get_crawl_tasks(db, skip=skip, limit=limit)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_admin_user)
):
    """删除任务（仅管理员）"""
    success = crud.delete_crawl_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
