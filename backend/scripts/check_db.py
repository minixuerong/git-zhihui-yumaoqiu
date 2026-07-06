"""检查 jobs 表结构"""
import sqlite3
conn = sqlite3.connect('backend/capability_graph.db')
c = conn.cursor()
c.execute("PRAGMA table_info(jobs)")
cols = c.fetchall()
for col in cols:
    print(f'  {col[1]} ({col[2]})')

c.execute("SELECT id, name FROM jobs LIMIT 30")
rows = c.fetchall()
print(f'\n前30条:')
for r in rows:
    print(f'  id={r[0]}, name="{r[1]}"')

conn.close()
