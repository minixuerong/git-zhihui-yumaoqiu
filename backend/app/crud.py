from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from datetime import datetime
from . import models
from . import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(
        models.User.username == username,
        models.User.is_deleted == False
    ).first()

def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(
        models.User.id == user_id,
        models.User.is_deleted == False
    ).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list:
    return db.query(models.User).filter(
        models.User.is_deleted == False
    ).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        role=user.role or models.UserRole.user
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ===== Admin =====

def get_admin_by_username(db: Session, username: str) -> models.Admin:
    return db.query(models.Admin).filter(
        models.Admin.username == username,
        models.Admin.is_active == True
    ).first()

def admin_exists(db: Session) -> bool:
    return db.query(models.Admin).filter(models.Admin.is_active == True).first() is not None

def create_admin(db: Session, username: str, password: str) -> models.Admin:
    hashed_password = get_password_hash(password)
    db_admin = models.Admin(
        username=username,
        password_hash=hashed_password
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> models.User:
    db_user = get_user(db, user_id)
    if db_user:
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.full_name is not None:
            db_user.full_name = user_update.full_name
        if user_update.role is not None:
            db_user.role = user_update.role
        if user_update.is_active is not None:
            db_user.is_active = user_update.is_active
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user:
        db_user.is_deleted = True
        db.commit()
        return True
    return False

def get_job_category(db: Session, category_id: int) -> models.JobCategory:
    return db.query(models.JobCategory).filter(
        models.JobCategory.id == category_id,
        models.JobCategory.is_deleted == False
    ).first()

def get_job_categories(db: Session, skip: int = 0, limit: int = 100) -> list:
    return db.query(models.JobCategory).filter(
        models.JobCategory.is_deleted == False
    ).offset(skip).limit(limit).all()

def create_job_category(db: Session, category: schemas.JobCategoryBase) -> models.JobCategory:
    db_category = models.JobCategory(
        name=category.name,
        parent_id=category.parent_id,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_job(db: Session, job_id: int) -> models.Job:
    return db.query(models.Job).filter(
        models.Job.id == job_id,
        models.Job.is_deleted == False
    ).first()

def get_job_by_code(db: Session, code: str) -> models.Job:
    return db.query(models.Job).filter(
        models.Job.code == code,
        models.Job.is_deleted == False,
        models.Job.data_type == 'raw'
    ).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 100, category_id: int = None,
             status: str = None, keyword: str = None, new_only: bool = False,
             data_type: str = None) -> list:
    query = db.query(models.Job).filter(models.Job.is_deleted == False)
    if data_type:
        query = query.filter(models.Job.data_type == data_type)
    if category_id:
        query = query.filter(models.Job.category_id == category_id)
    if status:
        query = query.filter(models.Job.status == status)
    if keyword:
        query = query.filter(or_(
            models.Job.name.contains(keyword),
            models.Job.code.contains(keyword)
        ))
    if new_only:
        today = datetime.now().date()
        query = query.filter(func.date(models.Job.created_at) == today)
    query = query.order_by(models.Job.created_at.desc())
    return query.offset(skip).limit(limit).all()

def get_jobs_count(db: Session, category_id: int = None, status: str = None, keyword: str = None, new_only: bool = False,
                   data_type: str = None) -> int:
    query = db.query(models.Job).filter(models.Job.is_deleted == False)
    if data_type:
        query = query.filter(models.Job.data_type == data_type)
    if category_id:
        query = query.filter(models.Job.category_id == category_id)
    if status:
        query = query.filter(models.Job.status == status)
    if keyword:
        query = query.filter(or_(
            models.Job.name.contains(keyword),
            models.Job.code.contains(keyword)
        ))
    if new_only:
        today = datetime.now().date()
        query = query.filter(func.date(models.Job.created_at) == today)
    return query.count()

def create_job(db: Session, job: schemas.JobCreate) -> models.Job:
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job(db: Session, job_id: int, job_update: schemas.JobUpdate) -> models.Job:
    db_job = get_job(db, job_id)
    if db_job:
        update_data = job_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: int) -> bool:
    db_job = get_job(db, job_id)
    if db_job:
        db_job.is_deleted = True
        db.commit()
        return True
    return False

def get_skill(db: Session, skill_id: int) -> models.Skill:
    return db.query(models.Skill).filter(
        models.Skill.id == skill_id,
        models.Skill.is_deleted == False
    ).first()

def get_skill_by_code(db: Session, code: str) -> models.Skill:
    return db.query(models.Skill).filter(
        models.Skill.code == code,
        models.Skill.is_deleted == False
    ).first()

def get_skills(db: Session, skip: int = 0, limit: int = 100, category: str = None,
               keyword: str = None) -> list:
    query = db.query(models.Skill).filter(models.Skill.is_deleted == False)
    if category:
        query = query.filter(models.Skill.category == category)
    if keyword:
        query = query.filter(or_(
            models.Skill.name.contains(keyword),
            models.Skill.code.contains(keyword)
        ))
    return query.offset(skip).limit(limit).all()

def get_skills_count(db: Session, category: str = None, keyword: str = None) -> int:
    query = db.query(models.Skill).filter(models.Skill.is_deleted == False)
    if category:
        query = query.filter(models.Skill.category == category)
    if keyword:
        query = query.filter(or_(
            models.Skill.name.contains(keyword),
            models.Skill.code.contains(keyword)
        ))
    return query.count()

def create_skill(db: Session, skill: schemas.SkillBase) -> models.Skill:
    db_skill = models.Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def update_skill(db: Session, skill_id: int, skill_update: dict) -> models.Skill:
    db_skill = get_skill(db, skill_id)
    if db_skill:
        for key, value in skill_update.items():
            setattr(db_skill, key, value)
        db.commit()
        db.refresh(db_skill)
    return db_skill

def delete_skill(db: Session, skill_id: int) -> bool:
    db_skill = get_skill(db, skill_id)
    if db_skill:
        db_skill.is_deleted = True
        db.commit()
        return True
    return False

def get_capability_requirements(db: Session, job_id: int) -> list:
    return db.query(models.CapabilityRequirement).filter(
        models.CapabilityRequirement.job_id == job_id
    ).all()

def create_capability_requirement(db: Session, req: schemas.CapabilityRequirementBase, job_id: int) -> models.CapabilityRequirement:
    db_req = models.CapabilityRequirement(**req.dict(), job_id=job_id)
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

def get_resume(db: Session, resume_id: int) -> models.Resume:
    return db.query(models.Resume).filter(
        models.Resume.id == resume_id,
        models.Resume.is_deleted == False
    ).first()

def get_resumes(db: Session, skip: int = 0, limit: int = 100, uploader_id: int = None) -> list:
    query = db.query(models.Resume).filter(models.Resume.is_deleted == False)
    if uploader_id:
        query = query.filter(models.Resume.uploader_id == uploader_id)
    return query.offset(skip).limit(limit).all()

def get_pending_resumes(db: Session, skip: int = 0, limit: int = 10) -> list:
    """获取待解析的简历（供 AI 模型拉取）"""
    return db.query(models.Resume).filter(
        models.Resume.is_deleted == False,
        models.Resume.status == 'pending'
    ).offset(skip).limit(limit).all()

def update_resume_parsed(db: Session, resume_id: int, parsed_data: str, parsed_skills: str = None) -> models.Resume:
    """AI 模型回写解析结果后更新"""
    db_resume = get_resume(db, resume_id)
    if db_resume:
        db_resume.status = 'parsed'
        db_resume.parsed_data = parsed_data
        db_resume.parsed_at = datetime.now()
        if parsed_skills:
            db_resume.parsed_skills = parsed_skills
        db.commit()
        db.refresh(db_resume)
    return db_resume

def create_resume(db: Session, resume: schemas.ResumeCreate, uploader_id: int) -> models.Resume:
    db_resume = models.Resume(**resume.dict(), uploader_id=uploader_id)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def update_resume_status(db: Session, resume_id: int, status: str) -> models.Resume:
    db_resume = get_resume(db, resume_id)
    if db_resume:
        db_resume.status = status
        db.commit()
        db.refresh(db_resume)
    return db_resume

def delete_resume(db: Session, resume_id: int) -> bool:
    db_resume = get_resume(db, resume_id)
    if db_resume:
        db_resume.is_deleted = True
        db.commit()
        return True
    return False

def get_resume_skills(db: Session, resume_id: int) -> list:
    return db.query(models.ResumeSkill).filter(
        models.ResumeSkill.resume_id == resume_id
    ).all()

def create_resume_skill(db: Session, skill: schemas.ResumeSkillBase, resume_id: int) -> models.ResumeSkill:
    db_skill = models.ResumeSkill(**skill.dict(), resume_id=resume_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def create_match_record(db: Session, record: schemas.MatchRecordBase) -> models.MatchRecord:
    db_record = models.MatchRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_match_records(db: Session, skip: int = 0, limit: int = 100,
                      resume_id: int = None, job_id: int = None) -> list:
    query = db.query(models.MatchRecord)
    if resume_id:
        query = query.filter(models.MatchRecord.resume_id == resume_id)
    if job_id:
        query = query.filter(models.MatchRecord.job_id == job_id)
    return query.offset(skip).limit(limit).all()

def get_match_record(db: Session, match_id: int) -> models.MatchRecord:
    return db.query(models.MatchRecord).filter(
        models.MatchRecord.id == match_id
    ).first()

def get_job_evolutions(db: Session, job_id: int) -> list:
    return db.query(models.JobEvolution).filter(
        models.JobEvolution.job_id == job_id
    ).order_by(models.JobEvolution.created_at.desc()).all()

def create_job_evolution(db: Session, evolution: schemas.JobEvolutionBase, job_id: int) -> models.JobEvolution:
    db_evolution = models.JobEvolution(**evolution.dict(), job_id=job_id)
    db.add(db_evolution)
    db.commit()
    db.refresh(db_evolution)
    return db_evolution

def get_ai_analysis_result(db: Session, result_id: int) -> models.AIAnalysisResult:
    return db.query(models.AIAnalysisResult).filter(
        models.AIAnalysisResult.id == result_id
    ).first()

def get_ai_analysis_results(db: Session, skip: int = 0, limit: int = 100, job_id: int = None) -> list:
    query = db.query(models.AIAnalysisResult)
    if job_id:
        query = query.filter(models.AIAnalysisResult.job_id == job_id)
    return query.offset(skip).limit(limit).all()

def create_ai_analysis_result(db: Session, result: schemas.AIAnalysisResultBase) -> models.AIAnalysisResult:
    db_result = models.AIAnalysisResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def create_crawl_task(db: Session, task: schemas.CrawlTaskBase) -> models.CrawlTask:
    db_task = models.CrawlTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_crawl_task_status(db: Session, task_id: str, status: str) -> models.CrawlTask:
    db_task = db.query(models.CrawlTask).filter(
        models.CrawlTask.task_id == task_id
    ).first()
    if db_task:
        db_task.status = status
        if status == "completed":
            db_task.analysis_time = datetime.now()
        db.commit()
        db.refresh(db_task)
    return db_task

def get_all_evolutions(db: Session, skip: int = 0, limit: int = 20) -> list:
    return db.query(models.JobEvolution).join(
        models.Job, models.JobEvolution.job_id == models.Job.id
    ).filter(
        models.Job.is_deleted == False
    ).order_by(
        models.JobEvolution.created_at.desc()
    ).offset(skip).limit(limit).all()

def get_users_count(db: Session) -> int:
    return db.query(models.User).filter(
        models.User.is_deleted == False
    ).count()

def get_crawl_tasks(db: Session, skip: int = 0, limit: int = 100) -> list:
    return db.query(models.CrawlTask).order_by(
        models.CrawlTask.created_at.desc()
    ).offset(skip).limit(limit).all()

def delete_crawl_task(db: Session, task_id: int) -> bool:
    db_task = db.query(models.CrawlTask).filter(
        models.CrawlTask.id == task_id
    ).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False