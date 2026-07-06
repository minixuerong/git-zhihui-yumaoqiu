from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from . import models
from .database import engine
from .routers import users, jobs, skills, resumes, match, crawler, cleaner, analysis, admin, graph, capabilities

load_dotenv()

models.Base.metadata.create_all(bind=engine)

API_V1_STR = os.getenv("API_V1_STR", "/api/v1")

app = FastAPI(
    title="多源异构数据驱动岗位和能力图谱构建与动态演化分析研究",
    description="基于FastAPI的后端服务，用于构建岗位和能力图谱",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(skills.router)
app.include_router(resumes.router)
app.include_router(match.router)
app.include_router(crawler.router)
app.include_router(cleaner.router)
app.include_router(analysis.router)
app.include_router(admin.router)
app.include_router(graph.router)
app.include_router(capabilities.router)

@app.get("/")
def read_root():
    return {"message": "多源异构数据驱动岗位和能力图谱构建与动态演化分析研究 - 后端服务"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "capability-graph-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)