import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app
from app.database import engine, Base

client = TestClient(app)

def cleanup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def setup():
    cleanup_db()
    yield

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "capability-graph-api"}

def test_welcome_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "多源异构数据驱动岗位和能力图谱" in response.json()["message"]

def test_user_register():
    response = client.post(
        "/api/v1/users/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_user_register_duplicate():
    client.post(
        "/api/v1/users/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    response = client.post(
        "/api/v1/users/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_user_login():
    client.post(
        "/api/v1/users/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    response = client.post(
        "/api/v1/users/login",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_user_login_invalid():
    client.post(
        "/api/v1/users/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    response = client.post(
        "/api/v1/users/login",
        json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def get_token():
    client.post(
        "/api/v1/users/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    login_response = client.post(
        "/api/v1/users/login",
        json={"username": "testuser", "password": "testpassword"}
    )
    return login_response.json()["access_token"]

def test_user_me():
    token = get_token()
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_user_list():
    token = get_token()
    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_user_detail():
    token = get_token()
    response = client.get(
        "/api/v1/users/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_user_update():
    token = get_token()
    response = client.put(
        "/api/v1/users/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "测试用户", "email": "new@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "测试用户"

def test_user_delete():
    token = get_token()
    response = client.delete(
        "/api/v1/users/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

def test_job_create():
    token = get_token()
    response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "测试工程师",
            "code": "TEST-001",
            "department": "测试部",
            "core_responsibilities": "负责测试工作"
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "测试工程师"

def test_job_create_duplicate_code():
    token = get_token()
    client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "测试工程师", "code": "TEST-001"}
    )
    response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "测试工程师2", "code": "TEST-001"}
    )
    assert response.status_code == 400

def test_job_list():
    token = get_token()
    response = client.get(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "items" in response.json()

def test_job_detail():
    token = get_token()
    create_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "开发工程师", "code": "DEV-001"}
    )
    job_id = create_response.json()["id"]
    response = client.get(
        f"/api/v1/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == job_id

def test_job_update():
    token = get_token()
    create_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "开发工程师", "code": "DEV-001"}
    )
    job_id = create_response.json()["id"]
    response = client.put(
        f"/api/v1/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "高级开发工程师", "department": "技术部"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "高级开发工程师"

def test_job_delete():
    token = get_token()
    create_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "待删除岗位", "code": "DEL-001"}
    )
    job_id = create_response.json()["id"]
    response = client.delete(
        f"/api/v1/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

def test_job_evolutions_list():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "产品经理", "code": "PM-001"}
    )
    job_id = job_response.json()["id"]
    response = client.get(
        f"/api/v1/jobs/{job_id}/evolutions",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_skill_create():
    token = get_token()
    response = client.post(
        "/api/v1/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Python", "code": "SKILL-PY"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Python"

def test_skill_list():
    token = get_token()
    response = client.get(
        "/api/v1/skills/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "items" in response.json()

def test_skill_detail():
    token = get_token()
    create_response = client.post(
        "/api/v1/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Java", "code": "SKILL-JAVA"}
    )
    skill_id = create_response.json()["id"]
    response = client.get(
        f"/api/v1/skills/{skill_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == skill_id

def test_skill_update():
    token = get_token()
    create_response = client.post(
        "/api/v1/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Java", "code": "SKILL-JAVA"}
    )
    skill_id = create_response.json()["id"]
    response = client.put(
        f"/api/v1/skills/{skill_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Java EE", "category": "后端"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Java EE"

def test_skill_delete():
    token = get_token()
    create_response = client.post(
        "/api/v1/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "待删除技能", "code": "DEL-SKILL"}
    )
    skill_id = create_response.json()["id"]
    response = client.delete(
        f"/api/v1/skills/{skill_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

def test_capability_requirement():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "数据工程师", "code": "DATA-001"}
    )
    job_id = job_response.json()["id"]
    skill_response = client.post(
        "/api/v1/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "SQL", "code": "SKILL-SQL"}
    )
    skill_id = skill_response.json()["id"]
    response = client.post(
        f"/api/v1/jobs/{job_id}/capabilities",
        headers={"Authorization": f"Bearer {token}"},
        json={"skill_id": skill_id, "requirement_type": "required", "level_required": "intermediate"}
    )
    assert response.status_code == 201
    assert response.json()["skill_id"] == skill_id

def test_capability_requirements_list():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "数据工程师", "code": "DATA-001"}
    )
    job_id = job_response.json()["id"]
    response = client.get(
        f"/api/v1/jobs/{job_id}/capabilities",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_job_evolution():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "产品经理", "code": "PM-001"}
    )
    job_id = job_response.json()["id"]
    response = client.post(
        f"/api/v1/jobs/{job_id}/evolutions",
        headers={"Authorization": f"Bearer {token}"},
        json={"changes_summary": "新增岗位", "evolution_type": "new"}
    )
    assert response.status_code == 201
    assert response.json()["job_id"] == job_id

def test_crawler_submit():
    response = client.post(
        "/api/v1/crawler/submit",
        json={
            "jobs": [
                {
                    "name": "爬虫测试岗位",
                    "code": "CRAWLER-TEST",
                    "department": "爬虫部"
                }
            ]
        }
    )
    assert response.status_code == 200
    assert response.json()["created_count"] >= 1

def test_cleaner_submit():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "待清洗岗位", "code": "CLEAN-TEST"}
    )
    job_id = job_response.json()["id"]
    response = client.post(
        "/api/v1/cleaner/submit",
        json={
            "job_id": job_id,
            "cleaned_data": {
                "department": "清洗后的部门",
                "core_responsibilities": "清洗后的职责"
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["job_id"] == job_id

def test_analysis_submit():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "分析测试岗位", "code": "ANALYSIS-TEST"}
    )
    job_id = job_response.json()["id"]
    response = client.post(
        "/api/v1/analysis/submit",
        json={
            "job_id": job_id,
            "analysis_result": "{\"capabilities\": []}",
            "confidence": 0.95,
            "model_version": "v1.0"
        }
    )
    assert response.status_code == 201
    assert response.json()["job_id"] == job_id

def test_analysis_get_cleaned_data():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "数据分析岗位", "code": "DATA-ANALYSIS"}
    )
    job_id = job_response.json()["id"]
    response = client.get(f"/api/v1/analysis/jobs/{job_id}/cleaned")
    assert response.status_code == 200
    assert response.json()["job_id"] == job_id

def test_analysis_results_list():
    token = get_token()
    response = client.get(
        "/api/v1/analysis/results",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_analysis_result_detail():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "分析岗位", "code": "ANALYSIS-DETAIL"}
    )
    job_id = job_response.json()["id"]
    create_response = client.post(
        "/api/v1/analysis/submit",
        json={
            "job_id": job_id,
            "analysis_result": "{\"capabilities\": []}",
            "confidence": 0.95,
            "model_version": "v1.0"
        }
    )
    result_id = create_response.json()["id"]
    response = client.get(
        f"/api/v1/analysis/results/{result_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == result_id

def test_resume_upload():
    token = get_token()
    response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", "test content")}
    )
    assert response.status_code == 201
    assert "id" in response.json()

def test_resume_list():
    token = get_token()
    response = client.get(
        "/api/v1/resumes/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_resume_detail():
    token = get_token()
    create_response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", "test content")}
    )
    resume_id = create_response.json()["id"]
    response = client.get(
        f"/api/v1/resumes/{resume_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == resume_id

def test_resume_skills_list():
    token = get_token()
    create_response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", "test content")}
    )
    resume_id = create_response.json()["id"]
    response = client.get(
        f"/api/v1/resumes/{resume_id}/skills",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_resume_add_skill():
    token = get_token()
    resume_response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", "test content")}
    )
    resume_id = resume_response.json()["id"]
    skill_response = client.post(
        "/api/v1/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Python", "code": "SKILL-PY-RESUME"}
    )
    skill_id = skill_response.json()["id"]
    response = client.post(
        f"/api/v1/resumes/{resume_id}/skills",
        headers={"Authorization": f"Bearer {token}"},
        json={"skill_id": skill_id, "level": "intermediate"}
    )
    assert response.status_code == 201
    assert response.json()["skill_id"] == skill_id

def test_resume_delete():
    token = get_token()
    create_response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", "test content")}
    )
    resume_id = create_response.json()["id"]
    response = client.delete(
        f"/api/v1/resumes/{resume_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

def test_match_analysis():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "匹配测试岗位", "code": "MATCH-TEST"}
    )
    job_id = job_response.json()["id"]
    skill_response = client.post(
        "/api/v1/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "匹配测试技能", "code": "MATCH-SKILL"}
    )
    skill_id = skill_response.json()["id"]
    client.post(
        f"/api/v1/jobs/{job_id}/capabilities",
        headers={"Authorization": f"Bearer {token}"},
        json={"skill_id": skill_id, "requirement_type": "required", "level_required": "beginner"}
    )
    resume_response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", "test content")}
    )
    resume_id = resume_response.json()["id"]
    response = client.post(
        "/api/v1/match/analysis",
        headers={"Authorization": f"Bearer {token}"},
        json={"resume_id": resume_id, "job_id": job_id}
    )
    assert response.status_code == 200
    assert "match_score" in response.json()

def test_match_records_list():
    token = get_token()
    response = client.get(
        "/api/v1/match/records",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_match_record_detail():
    token = get_token()
    job_response = client.post(
        "/api/v1/jobs/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "匹配记录岗位", "code": "MATCH-RECORD"}
    )
    job_id = job_response.json()["id"]
    skill_response = client.post(
        "/api/v1/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "匹配记录技能", "code": "MATCH-RECORD-SKILL"}
    )
    skill_id = skill_response.json()["id"]
    client.post(
        f"/api/v1/jobs/{job_id}/capabilities",
        headers={"Authorization": f"Bearer {token}"},
        json={"skill_id": skill_id, "requirement_type": "required", "level_required": "beginner"}
    )
    resume_response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", "test content")}
    )
    resume_id = resume_response.json()["id"]
    match_response = client.post(
        "/api/v1/match/analysis",
        headers={"Authorization": f"Bearer {token}"},
        json={"resume_id": resume_id, "job_id": job_id}
    )
    response = client.get(
        "/api/v1/match/records/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200