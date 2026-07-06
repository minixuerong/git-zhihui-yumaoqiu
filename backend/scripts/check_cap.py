"""检查 capability_requirements 和关联数据"""
import sqlite3, os
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'capability_graph.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

# 查看能力需求
c.execute("SELECT COUNT(*) FROM capability_requirements")
total = c.fetchone()[0]
print(f'capability_requirements 总数: {total}')

c.execute("""
    SELECT cr.id, cr.job_id, j.name, cr.skill_id, s.name, cr.importance_score
    FROM capability_requirements cr
    LEFT JOIN jobs j ON cr.job_id = j.id
    LEFT JOIN skills s ON cr.skill_id = s.id
    LIMIT 10
""")
rows = c.fetchall()
if rows:
    for r in rows:
        print(f'  id={r[0]}, job_id={r[1]}, job="{r[2]}", skill_id={r[3]}, skill="{r[4]}", score={r[5]}')
else:
    print('  (空)')

# 看看哪些 job_id 是有效的
c.execute("SELECT DISTINCT cr.job_id FROM capability_requirements cr LEFT JOIN jobs j ON cr.job_id=j.id WHERE j.id IS NULL")
orphan = c.fetchall()
if orphan:
    print(f'\n孤儿记录 (job_id 不存在于 jobs 表): {len(orphan)}')
    for o in orphan:
        print(f'  job_id={o[0]}')
else:
    print('\n所有 job_id 都有对应的 jobs 记录')

conn.close()
