"""检查9个图谱岗位是否在jobs表中"""
import sys
sys.path.insert(0, '.')
from app.database import SessionLocal

db = SessionLocal()
names = ['AI算法工程师', '算法工程师', '智能驾驶算法工程师', 'CAE算法工程师', 
         '人工智能工程师', 'AI算法工程师助理', '机器视觉工程师', 
         '人工智能研发工程师', 'AI软件工程师']

for n in names:
    rows = db.execute(f"SELECT id, name FROM jobs WHERE name = '{n}' LIMIT 1").fetchall()
    if rows:
        print(f'FOUND: id={rows[0][0]}, name="{rows[0][1]}"')
    else:
        print(f'MISSING: "{n}"')
db.close()
