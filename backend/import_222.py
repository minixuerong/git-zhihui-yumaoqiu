"""导入 222.json 爬虫数据到 jobs 表"""
import json
import hashlib
from datetime import datetime
from app.database import SessionLocal
from app.models import Job
from app.schemas import JobCreate
from app import crud

db = SessionLocal()
try:
    with open("../222.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    created = 0
    skipped = 0
    for item in raw_data:
        # 生成唯一 code：取 URL 的 MD5 前 16 位
        url = item.get("url", "")
        code = hashlib.md5(url.encode()).hexdigest()[:16]

        # 检查是否已存在
        existing = crud.get_job_by_code(db, code=code)
        if existing:
            skipped += 1
            continue

        job = JobCreate(
            name=item.get("job_title", "").strip(),
            code=code,
            department=item.get("company", "").strip(),
            core_responsibilities=item.get("jd", "").strip(),
            data_source=url,
            # 从 update_date 取日期，判断是否为今日
            is_new=False,  # 昨日的岗位
            status="active"
        )
        crud.create_job(db, job=job)
        created += 1

    print(f"导入完成：新增 {created} 条，跳过（已存在）{skipped} 条")
    print(f"jobs 表现在共有 {db.query(Job).count()} 条记录")
finally:
    db.close()
