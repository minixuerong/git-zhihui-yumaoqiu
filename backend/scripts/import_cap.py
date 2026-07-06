"""直接从 graph_data.json 插入所有关联到 capability_requirements"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app import models

db = SessionLocal()

graph_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src', 'assets', 'graph_data.json')
with open(graph_path, encoding='utf-8') as f:
    graph = json.load(f)

all_jobs = {j.name.strip(): j.id for j in db.query(models.Job).filter(models.Job.is_deleted == False).all()}
all_skills = {s.name.strip(): s.id for s in db.query(models.Skill).filter(models.Skill.is_deleted == False).all()}

print(f'DB jobs: {len(all_jobs)} -> {list(all_jobs.keys())}')
print(f'DB skills: {len(all_skills)}')

existing_ids = {(cr.job_id, cr.skill_id) for cr in db.query(models.CapabilityRequirement).all()}
print(f'已有 capability: {len(existing_ids)}')

created = 0
skipped = 0
for link in graph.get('links', []):
    job_name = link['source']
    skill_name = link['target']
    job_id = all_jobs.get(job_name)
    skill_id = all_skills.get(skill_name)
    
    if not job_id:
        print(f'  跳过岗位: {job_name}')
        skipped += 1
        continue
    if not skill_id:
        print(f'  跳过技能: {skill_name}')
        skipped += 1
        continue
    if (job_id, skill_id) in existing_ids:
        skipped += 1
        continue
    
    cr = models.CapabilityRequirement(
        job_id=job_id, skill_id=skill_id,
        requirement_type='required',
        importance_score=min(link.get('value', 1) / 10, 1.0)
    )
    db.add(cr)
    created += 1

if created:
    db.commit()
print(f'\n新增: {created}, 跳过: {skipped}')
print(f'capability_requirements 总数: {db.query(models.CapabilityRequirement).count()}')
db.close()
