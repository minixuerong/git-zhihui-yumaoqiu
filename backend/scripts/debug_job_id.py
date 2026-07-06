"""检查job_id=1637是什么"""
import sys; sys.path.insert(0, '.')
from app.database import SessionLocal

db = SessionLocal()
row = db.execute("SELECT id, name FROM jobs WHERE id = 1637").fetchone()
print(f'job_id=1637: id={row[0]}, name="{row[1]}"' if row else 'job_id=1637 not found')

# Also check id=789
row2 = db.execute("SELECT id, name FROM jobs WHERE id = 789").fetchone()
print(f'job_id=789: id={row2[0]}, name="{row2[1]}"' if row2 else 'job_id=789 not found')

# Count capability_requirements by job_id
rows = db.execute("""
    SELECT j.name, COUNT(cr.id) as cnt 
    FROM capability_requirements cr 
    JOIN jobs j ON cr.job_id = j.id 
    GROUP BY j.id, j.name 
    ORDER BY cnt DESC
    LIMIT 20
""").fetchall()
print('\nTop 20 jobs by capability count:')
for r in rows:
    print(f'  id="?", name="{r[0]}", count={r[1]}')

db.close()
