"""能力需求（岗位-技能关联）CRUD API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from ..database import get_db
from .. import models, schemas, crud

router = APIRouter(prefix="/api/v1/capabilities", tags=["capabilities"])


@router.get("/")
def list_capabilities(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    job_id: Optional[int] = None,
    skill_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """分页查询所有能力需求，包含岗位名和技能名"""
    query = db.query(
        models.CapabilityRequirement,
        models.Job.name.label("job_name"),
        models.Skill.name.label("skill_name")
    ).join(
        models.Job, models.CapabilityRequirement.job_id == models.Job.id
    ).join(
        models.Skill, models.CapabilityRequirement.skill_id == models.Skill.id
    ).filter(
        models.Job.is_deleted == False,
        models.Skill.is_deleted == False
    )

    if job_id is not None:
        query = query.filter(models.CapabilityRequirement.job_id == job_id)
    if skill_id is not None:
        query = query.filter(models.CapabilityRequirement.skill_id == skill_id)

    total = query.count()
    rows = query.order_by(
        models.CapabilityRequirement.id.desc()
    ).offset(skip).limit(limit).all()

    items = []
    for cr, job_name, skill_name in rows:
        items.append({
            "id": cr.id,
            "job_id": cr.job_id,
            "skill_id": cr.skill_id,
            "job_name": job_name,
            "skill_name": skill_name,
            "requirement_type": cr.requirement_type,
            "level_required": cr.level_required,
            "importance_score": cr.importance_score,
            "created_at": cr.created_at.isoformat() if cr.created_at else None
        })

    return {"items": items, "total": total, "page": skip // limit + 1, "size": limit}


@router.post("/")
def create_capability(
    req: schemas.CapabilityRequirementBase,
    job_id: int = Query(..., description="岗位ID"),
    db: Session = Depends(get_db)
):
    """创建能力需求（岗位关联技能）"""
    # 检查岗位存在
    job = db.query(models.Job).filter(models.Job.id == job_id, models.Job.is_deleted == False).first()
    if not job:
        raise HTTPException(404, detail="岗位不存在")

    # 检查技能存在
    skill = db.query(models.Skill).filter(models.Skill.id == req.skill_id, models.Skill.is_deleted == False).first()
    if not skill:
        raise HTTPException(404, detail="技能不存在")

    # 检查是否已存在
    existing = db.query(models.CapabilityRequirement).filter(
        models.CapabilityRequirement.job_id == job_id,
        models.CapabilityRequirement.skill_id == req.skill_id
    ).first()
    if existing:
        raise HTTPException(400, detail="该岗位已关联此技能")

    cr = crud.create_capability_requirement(db, req=req, job_id=job_id)
    return {
        "id": cr.id,
        "job_id": cr.job_id,
        "skill_id": cr.skill_id,
        "job_name": job.name,
        "skill_name": skill.name,
        "requirement_type": cr.requirement_type,
        "level_required": cr.level_required,
        "importance_score": cr.importance_score,
        "created_at": cr.created_at.isoformat() if cr.created_at else None,
    }


@router.put("/{capability_id}")
def update_capability(
    capability_id: int,
    data: schemas.CapabilityRequirementBase,
    db: Session = Depends(get_db)
):
    """更新能力需求"""
    cr = db.query(models.CapabilityRequirement).filter(models.CapabilityRequirement.id == capability_id).first()
    if not cr:
        raise HTTPException(404, detail="能力需求不存在")

    cr.requirement_type = data.requirement_type
    cr.level_required = data.level_required
    cr.importance_score = data.importance_score
    db.commit()
    db.refresh(cr)

    job = db.query(models.Job).filter(models.Job.id == cr.job_id).first()
    skill = db.query(models.Skill).filter(models.Skill.id == cr.skill_id).first()
    return {
        "id": cr.id,
        "job_id": cr.job_id,
        "skill_id": cr.skill_id,
        "job_name": job.name if job else "",
        "skill_name": skill.name if skill else "",
        "requirement_type": cr.requirement_type,
        "level_required": cr.level_required,
        "importance_score": cr.importance_score,
        "created_at": cr.created_at.isoformat() if cr.created_at else None,
    }


@router.delete("/{capability_id}")
def delete_capability(capability_id: int, db: Session = Depends(get_db)):
    """删除能力需求"""
    cr = db.query(models.CapabilityRequirement).filter(models.CapabilityRequirement.id == capability_id).first()
    if not cr:
        raise HTTPException(404, detail="能力需求不存在")
    db.delete(cr)
    db.commit()
    return {"message": "删除成功"}
