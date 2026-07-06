"""导入 graph_data.json 的关联数据到 capability_requirements 表"""
import sys
import json
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app import models

db = SessionLocal()

try:
    # 读取 graph_data.json
    graph_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src', 'assets', 'graph_data.json')
    with open(graph_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)

    # 构建 skills 名称→id 映射
    all_skills = db.query(models.Skill).filter(models.Skill.is_deleted == False).all()
    skill_map = {s.name.strip(): s.id for s in all_skills}
    
    # 构建 jobs 名称→id 映射（优先精确匹配，再模糊匹配）
    all_jobs = db.query(models.Job).filter(models.Job.is_deleted == False).all()
    
    def find_job_id(name):
        """按名称找岗位，先精确匹配，再 LIKE 匹配"""
        name = name.strip()
        # 1. 精确匹配
        for j in all_jobs:
            if j.name.strip() == name:
                return j.id
        # 2. 包含匹配（取最短的）
        candidates = [j for j in all_jobs if name in j.name]
        if candidates:
            candidates.sort(key=lambda x: len(x.name))
            return candidates[0].id
        return None

    # 读取已有的 capability_requirements（避免重复）
    existing = set()
    for cr in db.query(models.CapabilityRequirement).all():
        existing.add((cr.job_id, cr.skill_id))

    created = 0
    skipped = 0
    link_count = len(graph_data.get('links', []))
    
    for link in graph_data.get('links', []):
        job_name = link['source']
        skill_name = link['target']
        value = link.get('value', 1)
        
        job_id = find_job_id(job_name)
        skill_id = skill_map.get(skill_name.strip())
        
        if not job_id:
            print(f"  ⚠ 未找到岗位: {job_name}")
            skipped += 1
            continue
        if not skill_id:
            print(f"  ⚠ 未找到技能: {skill_name}")
            skipped += 1
            continue
        
        if (job_id, skill_id) in existing:
            skipped += 1
            continue
        
        # value 1→0.2, 2→0.4, 3→0.6
        importance = value * 0.2
        
        cr = models.CapabilityRequirement(
            job_id=job_id,
            skill_id=skill_id,
            requirement_type='required',
            importance_score=importance
        )
        db.add(cr)
        existing.add((job_id, skill_id))
        created += 1

    db.commit()
    
    print(f"\n导入完成！")
    print(f"  graph_data.json 总关联数: {link_count}")
    print(f"  新增 capability_requirements: {created}")
    print(f"  跳过（已存在或未匹配）: {skipped}")
    print(f"  capability_requirements 表现有总数: {db.query(models.CapabilityRequirement).count()}")

finally:
    db.close()
