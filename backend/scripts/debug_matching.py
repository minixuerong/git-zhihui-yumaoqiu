"""检查 _match_job_group 的匹配结果"""
import sys; sys.path.insert(0, '.')
from app.database import SessionLocal
import json, os

db = SessionLocal()

# Load graph job names from graph_data.json
graph_path = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src', 'assets', 'graph_data.json')
with open(graph_path, encoding='utf-8') as f:
    data = json.load(f)
graph_job_names = [n['name'] for n in data['nodes'] if n.get('category') != 8]

# Get all jobs from DB
all_jobs = db.execute("SELECT id, name FROM jobs WHERE is_deleted = 0").fetchall()
print(f'Total jobs in DB: {len(all_jobs)}')

# Check matching for each graph job name
for name in graph_job_names:
    exact = [j for j in all_jobs if j[1].strip() == name]
    partial = [j for j in all_jobs if name in j[1] and j[1].strip() != name]
    total = len(exact) + len(partial)
    print(f'\n"{name}": exact={len(exact)}, partial={len(partial)}, total={total}')
    if exact:
        for j in exact[:3]:
            print(f'  exact: id={j[0]}, name="{j[1]}"')
    if partial:
        for j in partial[:3]:
            print(f'  partial: id={j[0]}, name="{j[1]}"')

# Check id=1637 specifically
print('\n--- Checking id=1637 ---')
j1637 = [j for j in all_jobs if j[0] == 1637]
if j1637:
    print(f'id=1637: name="{j1637[0][1]}", repr={repr(j1637[0][1])}')
    
# Check id=789
j789 = [j for j in all_jobs if j[0] == 789]
if j789:
    print(f'id=789: name="{j789[0][1]}", repr={repr(j789[0][1])}')

# Compare the two
if j1637 and j789:
    print(f'Equal: {j1637[0][1] == j789[0][1]}')
    print(f'Equal strip: {j1637[0][1].strip() == j789[0][1].strip()}')

db.close()
