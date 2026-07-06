"""深入检查AI算法工程师的能力需求在图谱中丢失的原因"""
import sys; sys.path.insert(0, '.')
from app.database import SessionLocal
from app import models
import json, os

db = SessionLocal()

# Get all capability_requirements for AI算法工程师 jobs
graph_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src', 'assets', 'graph_data.json')
with open(graph_path, encoding='utf-8') as f:
    graph_data = json.load(f)
graph_job_names = [n['name'] for n in graph_data['nodes'] if n.get('category') != 8]

# Get all non-deleted jobs
all_jobs = db.query(models.Job).filter(models.Job.is_deleted == False).all()

# Find all job IDs for "AI算法工程师" (exact match)
ai_ids = [j.id for j in all_jobs if j.name.strip() == 'AI算法工程师']
print(f'AI算法工程师 exact match job IDs ({len(ai_ids)}): {ai_ids[:5]}...')

# Count capability_requirements for these jobs
cr_count = db.query(models.CapabilityRequirement).filter(
    models.CapabilityRequirement.job_id.in_(ai_ids)
).count()
print(f'Capability requirements for these jobs: {cr_count}')

# Check a few
crs = db.query(models.CapabilityRequirement).filter(
    models.CapabilityRequirement.job_id.in_(ai_ids)
).limit(5).all()
for cr in crs:
    skill = db.query(models.Skill).filter(models.Skill.id == cr.skill_id).first()
    print(f'  job_id={cr.job_id}, skill_id={cr.skill_id}, skill_name={skill.name if skill else "N/A"}, score={cr.importance_score}')

# Now check the graph matching logic
# Build job_id_to_graph_name
job_id_to_graph_name = {}
for name in graph_job_names:
    exact = [j for j in all_jobs if j.name.strip() == name]
    partial = [j for j in all_jobs if name in j.name and j.name.strip() != name]
    for j in exact:
        job_id_to_graph_name[j.id] = name
    for j in partial:
        job_id_to_graph_name[j.id] = name

# Check if ai_ids are in the map
print(f'\nAI algorithm engineer IDs in graph map:')
for jid in ai_ids[:10]:
    print(f'  job_id={jid} -> "{job_id_to_graph_name.get(jid, "NOT FOUND")}"')

# Now check all capability_requirements that should be linked to AI算法工程师
cr_db = db.query(models.CapabilityRequirement).filter(
    models.CapabilityRequirement.job_id.in_(ai_ids)
).all()

print(f'\nChecking {len(cr_db)} CRs for graph link creation:')
link_agg = {}
for cr in cr_db:
    graph_name = job_id_to_graph_name.get(cr.job_id)
    if not graph_name:
        print(f'  SKIP: job_id={cr.job_id} not in graph map')
        continue
    skill = db.query(models.Skill).filter(models.Skill.id == cr.skill_id).first()
    if not skill:
        print(f'  SKIP: skill_id={cr.skill_id} not found')
        continue
    key = ('job:' + graph_name, 'skill:' + skill.name)
    link_agg[key] = link_agg.get(key, 0) + 1

print(f'Created {len(link_agg)} link aggregates for AI算法工程师')
for (s, t), cnt in list(link_agg.items())[:5]:
    print(f'  {s} -> {t} (count={cnt})')

db.close()
