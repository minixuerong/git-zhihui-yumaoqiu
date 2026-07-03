from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .models import UserRole, JobStatus, DataJobType, SkillLevel, RequirementType, ResumeStatus, EvolutionType, CrawlTaskStatus

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: Optional[UserRole] = UserRole.user

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class AdminResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class JobCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    parent_id: Optional[int] = None
    description: Optional[str] = None

class JobCategoryResponse(JobCategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    code: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = None
    description: Optional[str] = None

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class SkillResponse(SkillBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CapabilityRequirementBase(BaseModel):
    skill_id: int
    requirement_type: RequirementType
    level_required: Optional[SkillLevel] = None
    importance_score: Optional[float] = Field(None, ge=0, le=1)

class CapabilityRequirementResponse(CapabilityRequirementBase):
    id: int
    job_id: int
    skill: SkillResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

class JobBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    code: str = Field(..., min_length=1, max_length=100)
    category_id: Optional[int] = None
    department: Optional[str] = None
    core_responsibilities: Optional[str] = None
    typical_scenarios: Optional[str] = None
    is_new: Optional[bool] = None
    status: Optional[JobStatus] = None
    data_source: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    data_type: Optional[DataJobType] = DataJobType.raw
    uploader_id: Optional[int] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    category_id: Optional[int] = None
    department: Optional[str] = None
    core_responsibilities: Optional[str] = None
    typical_scenarios: Optional[str] = None
    is_new: Optional[bool] = None
    status: Optional[JobStatus] = None
    data_source: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0, le=1)

class JobResponse(JobBase):
    id: int
    category: Optional[JobCategoryResponse] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ResumeBase(BaseModel):
    filename: str
    file_path: str
    content: Optional[str] = None
    parsed_skills: Optional[str] = None

class ResumeCreate(ResumeBase):
    pass

class ResumeResponse(ResumeBase):
    id: int
    uploader_id: Optional[int]
    status: ResumeStatus
    parsed_data: Optional[str] = None
    parsed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ResumeParseSubmit(BaseModel):
    """AI 模型回写简历解析结果的请求体"""
    parsed_data: str  # 解析结果 JSON 字符串
    parsed_skills: Optional[str] = None  # 提取的技能列表 JSON

class ResumeSkillBase(BaseModel):
    skill_id: int
    level: Optional[SkillLevel] = None
    confidence: Optional[float] = Field(None, ge=0, le=1)

class ResumeSkillResponse(ResumeSkillBase):
    id: int
    resume_id: int
    skill: SkillResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

class MatchRecordBase(BaseModel):
    resume_id: int
    job_id: int
    match_score: float = Field(..., ge=0, le=1)
    gap_analysis: Optional[str] = None
    improvement_suggestions: Optional[str] = None
    learning_path: Optional[str] = None

class MatchRecordResponse(MatchRecordBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MatchAnalysisRequest(BaseModel):
    resume_id: int
    job_id: int

class MatchAnalysisResponse(BaseModel):
    match_score: float
    gap_analysis: List[Dict[str, Any]]
    improvement_suggestions: List[str]
    learning_path: List[str]

class JobEvolutionBase(BaseModel):
    changes_summary: Optional[str] = None
    changed_fields: Optional[str] = None
    evolution_type: Optional[EvolutionType] = None

class JobEvolutionResponse(JobEvolutionBase):
    id: int
    job_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class JDDataSourceBase(BaseModel):
    name: str
    url: Optional[str] = None
    enabled: Optional[bool] = True

class JDDataSourceResponse(JDDataSourceBase):
    id: int
    last_crawl_time: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class CrawlTaskBase(BaseModel):
    task_id: str
    source_name: str
    source_url: Optional[str] = None

class CrawlTaskResponse(CrawlTaskBase):
    id: int
    status: CrawlTaskStatus
    crawl_time: Optional[datetime] = None
    clean_time: Optional[datetime] = None
    analysis_time: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class AIAnalysisResultBase(BaseModel):
    job_id: int
    analysis_result: str
    confidence: Optional[float] = Field(0.0, ge=0, le=1)
    model_version: Optional[str] = None
    analysis_time: Optional[datetime] = None

class AIAnalysisResultResponse(AIAnalysisResultBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CrawlerSubmitRequest(BaseModel):
    jobs: List[JobCreate]

class CrawlerSubmitResponse(BaseModel):
    message: str
    created_count: int
    updated_count: int

class CleanerSubmitRequest(BaseModel):
    job_id: int
    cleaned_data: Dict[str, Any]

class CleanerSubmitResponse(BaseModel):
    message: str
    job_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int

class DashboardStatsResponse(BaseModel):
    total_jobs: int
    total_skills: int
    total_users: int
    pending_updates: int
    today_new_jobs: int

class EvolutionWithJobResponse(BaseModel):
    id: int
    job_id: int
    job_name: Optional[str] = None
    changes_summary: Optional[str] = None
    changed_fields: Optional[str] = None
    evolution_type: Optional[EvolutionType] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CrawlTaskUpdate(BaseModel):
    status: Optional[str] = None
    source_name: Optional[str] = None
    source_url: Optional[str] = None