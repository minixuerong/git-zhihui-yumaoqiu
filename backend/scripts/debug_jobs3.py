"""检查 jobs 表中图谱岗位名"""
import json
import urllib.request

# 读取 graph_data.json 中的岗位名称
with open('frontend/src/assets/graph_data.json', encoding='utf-8') as f:
    graph = json.load(f)
    graph_names = [n['name'] for n in graph['nodes'] if n.get('category') != 8]
    print('图谱岗位名:', graph_names)

# 检查 jobs 表中匹配的记录
import sqlite3
conn = sqlite3.connect('backend/capability_graph.db')
c = conn.cursor()
for gn in graph_names:
    c.execute("SELECT id, name FROM jobs WHERE name LIKE ?", (f'%{gn}%',))
    rows = c.fetchall()
    if rows:
        for r in rows:
            print(f'  DB匹配: id={r[0]}, name="{r[1]}" ← 图谱名="{gn}"')
    else:
        print(f'  DB未找到: [{gn}]')
conn.close()
