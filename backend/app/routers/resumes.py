from typing import Optional
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from datetime import datetime

from .. import schemas
from .. import crud
from ..database import get_db
from .users import get_current_active_user, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/api/v1/resumes", tags=["resumes"])

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=schemas.ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    allowed_extensions = {".pdf", ".docx", ".doc", ".txt"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed. Only PDF, DOCX, DOC, TXT are supported."
        )
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    resume_create = schemas.ResumeCreate(
        filename=file.filename,
        file_path=file_path
    )
    
    return crud.create_resume(db=db, resume=resume_create, uploader_id=current_user.id)


# ===== AI 模型调用接口（无需登录） =====

@router.get("/pending", response_model=list[schemas.ResumeResponse],
            description="AI 模型拉取待解析的简历列表")
def get_pending_resumes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """AI 模型轮询此接口获取待解析的简历，拿到 resume_id 后下载文件、解析，再回写结果。"""
    return crud.get_pending_resumes(db, skip=skip, limit=limit)


@router.post("/{resume_id}/parse-result", response_model=schemas.ResumeResponse,
             description="AI 模型回写简历解析结果")
def submit_parse_result(
    resume_id: int,
    body: schemas.ResumeParseSubmit,
    db: Session = Depends(get_db)
):
    """AI 模型解析完成后调用此接口回写结果。
    
    - parsed_data: 完整解析结果的 JSON 字符串
    - parsed_skills: 技能列表 JSON（可选）
    """
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return crud.update_resume_parsed(
        db, resume_id=resume_id,
        parsed_data=body.parsed_data,
        parsed_skills=body.parsed_skills
    )

@router.get("/", response_model=list[schemas.ResumeResponse])
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 current_user: schemas.UserResponse = Depends(get_current_active_user)):
    """普通用户只能看自己的简历"""
    return crud.get_resumes(db, skip=skip, limit=limit, uploader_id=current_user.id)

@router.get("/{resume_id}", response_model=schemas.ResumeResponse)
def read_resume(resume_id: int, db: Session = Depends(get_db),
                current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None or db_resume.uploader_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume

@router.get("/{resume_id}/skills", response_model=list[schemas.ResumeSkillResponse])
def get_resume_skills(resume_id: int, db: Session = Depends(get_db),
                      current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return crud.get_resume_skills(db, resume_id=resume_id)

@router.post("/{resume_id}/skills", response_model=schemas.ResumeSkillResponse,
             status_code=status.HTTP_201_CREATED)
def add_resume_skill(resume_id: int, skill: schemas.ResumeSkillBase,
                     db: Session = Depends(get_db),
                     current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    db_skill = crud.get_skill(db, skill_id=skill.skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return crud.create_resume_skill(db, skill=skill, resume_id=resume_id)

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(resume_id: int, db: Session = Depends(get_db),
                  current_user: schemas.UserResponse = Depends(get_current_active_user)):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None or db_resume.uploader_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    crud.delete_resume(db, resume_id=resume_id)

@router.get("/{resume_id}/file")
def download_resume_file(resume_id: int, request: Request, db: Session = Depends(get_db),
                         token: Optional[str] = Query(None)):
    """查看/下载简历原始文件（支持新标签页打开）"""
    # 1. 从 Authorization header 取 token
    auth_header = request.headers.get("Authorization")
    access_token = token  # 先取 query param
    if auth_header and auth_header.startswith("Bearer "):
        access_token = auth_header[7:]  # header 优先
    # 2. 解码 token
    current_user = None
    if access_token:
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                from ..crud import get_user_by_username
                current_user = get_user_by_username(db, username)
        except JWTError:
            pass
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # 3. 校验权限
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None or db_resume.uploader_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    if not os.path.exists(db_resume.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    return FileResponse(
        db_resume.file_path,
        filename=db_resume.filename,
        media_type="application/octet-stream"
    )