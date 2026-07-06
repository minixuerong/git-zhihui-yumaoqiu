"""检查 jobs 表完整内容"""
import sqlite3, os
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'capability_graph.db')
db_path = os.path.normpath(db_path)
print(f'DB路径: {db_path}')
print(f'文件存在: {os.path.exists(db_path)}')
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM jobs")
total = c.fetchone()[0]
print(f'总岗位数: {total}')
c.execute("SELECT id, name FROM jobs LIMIT 50")
rows = c.fetchall()
for r in rows:
    print(f'  id={r[0]}, name="{r[1]}"')
conn.close()
