"""删除 jobs 表中所有岗位数据（级联删除关联表数据）"""
from app.database import SessionLocal
from app.models import Job

db = SessionLocal()
try:
    count = db.query(Job).filter(Job.is_deleted == False).count()
    print(f"当前有效岗位数: {count}")
    
    # 直接删除所有 Job 记录（级联删除关联表）
    deleted = db.query(Job).filter(Job.is_deleted == False).delete(synchronize_session=False)
    db.commit()
    print(f"成功删除 {deleted} 条岗位记录")
    
    # 确认剩余记录
    remaining = db.query(Job).count()
    print(f"jobs 表剩余总记录数: {remaining}")
finally:
    db.close()
