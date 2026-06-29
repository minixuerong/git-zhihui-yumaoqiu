from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"

class JobStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    deprecated = "deprecated"

class DataJobType(str, enum.Enum):
    raw = "raw"
    cleaned = "cleaned"

class SkillLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class RequirementType(str, enum.Enum):
    required = "required"
    preferred = "preferred"

class ResumeStatus(str, enum.Enum):
    pending = "pending"
    parsed = "parsed"
    analyzed = "analyzed"

class EvolutionType(str, enum.Enum):
    new = "new"
    update = "update"
    delete = "delete"
    category_change = "category_change"

class CrawlTaskStatus(str, enum.Enum):
    pending = "pending"
    cleaning = "cleaning"
    analyzing = "analyzing"
    completed = "completed"
    failed = "failed"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255))
    full_name = Column(String(200))
    role = Column(Enum(UserRole), default=UserRole.user)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    resumes = relationship("Resume", back_populates="uploader")

class JobCategory(Base):
    __tablename__ = "job_categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("job_categories.id"))
    description = Column(String(500))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    
    parent = relationship("JobCategory", remote_side=[id])
    jobs = relationship("Job", back_populates="category")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(100), nullable=False, unique=True, index=True)
    category = Column(String(100), index=True)
    description = Column(Text)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    capability_requirements = relationship("CapabilityRequirement", back_populates="skill")
    resume_skills = relationship("ResumeSkill", back_populates="skill")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    code = Column(String(100), nullable=False, unique=True, index=True)
    category_id = Column(Integer, ForeignKey("job_categories.id"))
    department = Column(String(200))
    core_responsibilities = Column(Text)
    typical_scenarios = Column(Text)
    is_new = Column(Boolean)
    status = Column(Enum(JobStatus))
    data_source = Column(String(500))
    confidence_score = Column(Float)
    is_deleted = Column(Boolean, default=False)
    data_type = Column(Enum(DataJobType), default=DataJobType.raw, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    category = relationship("JobCategory", back_populates="jobs")
    capability_requirements = relationship("CapabilityRequirement", back_populates="job", cascade="all, delete-orphan")
    evolutions = relationship("JobEvolution", back_populates="job", cascade="all, delete-orphan")
    match_records = relationship("MatchRecord", back_populates="job", cascade="all, delete-orphan")
    ai_analysis_results = relationship("AIAnalysisResult", back_populates="job", cascade="all, delete-orphan")

class CapabilityRequirement(Base):
    __tablename__ = "capability_requirements"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False, index=True)
    requirement_type = Column(Enum(RequirementType), nullable=False)
    level_required = Column(Enum(SkillLevel))
    importance_score = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    
    job = relationship("Job", back_populates="capability_requirements")
    skill = relationship("Skill", back_populates="capability_requirements")
    
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    content = Column(Text)
    parsed_skills = Column(Text)
    parsed_data = Column(Text)  # AI 模型回写的完整解析结果（JSON）
    parsed_at = Column(DateTime)  # 解析完成时间
    uploader_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(ResumeStatus), default=ResumeStatus.pending)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    uploader = relationship("User", back_populates="resumes")
    resume_skills = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
    match_records = relationship("MatchRecord", back_populates="resume", cascade="all, delete-orphan")

class ResumeSkill(Base):
    __tablename__ = "resume_skills"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False, index=True)
    level = Column(Enum(SkillLevel))
    confidence = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    
    resume = relationship("Resume", back_populates="resume_skills")
    skill = relationship("Skill", back_populates="resume_skills")

class MatchRecord(Base):
    __tablename__ = "match_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    match_score = Column(Float, nullable=False)
    gap_analysis = Column(Text)
    improvement_suggestions = Column(Text)
    learning_path = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    
    resume = relationship("Resume", back_populates="match_records")
    job = relationship("Job", back_populates="match_records")

class JobEvolution(Base):
    __tablename__ = "job_evolutions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    changes_summary = Column(String(500))
    changed_fields = Column(Text)
    evolution_type = Column(Enum(EvolutionType))
    created_at = Column(DateTime, server_default=func.now())
    
    job = relationship("Job", back_populates="evolutions")

class JDDataSource(Base):
    __tablename__ = "jd_data_sources"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    url = Column(String(500))
    enabled = Column(Boolean, default=True)
    last_crawl_time = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class CrawlTask(Base):
    __tablename__ = "crawl_tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(50), unique=True, index=True)
    source_name = Column(String(200), nullable=False)
    source_url = Column(String(500))
    status = Column(Enum(CrawlTaskStatus), default=CrawlTaskStatus.pending)
    crawl_time = Column(DateTime)
    clean_time = Column(DateTime)
    analysis_time = Column(DateTime)
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class AIAnalysisResult(Base):
    __tablename__ = "ai_analysis_results"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    analysis_result = Column(Text, nullable=False)
    confidence = Column(Float, default=0.0)
    model_version = Column(String(50))
    analysis_time = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    
    job = relationship("Job", back_populates="ai_analysis_results")