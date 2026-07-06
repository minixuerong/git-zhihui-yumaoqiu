"""将 graph_data.json 中的岗位同步到 jobs 表"""
import json, sqlite3, os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'capability_graph.db')
graph_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'frontend', 'src', 'assets', 'graph_data.json')

if not os.path.exists(graph_path):
    graph_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'frontend', 'src', 'assets', 'graph_data.json')

print(f'DB: {db_path}')
print(f'Graph: {graph_path}')

# 读取 graph_data.json
with open(graph_path, encoding='utf-8') as f:
    graph = json.load(f)

job_nodes = [n for n in graph['nodes'] if n.get('category') != 8]
print(f'图谱岗位数: {len(job_nodes)}')

# category index → DB category_id
# 图谱 categories: [底层研发(0), 算法模型(1), 数据(2), 产品应用(3), 硬件(4), 测试运维(5), 设计(6), 项目管理(7), 技能(8)]
# DB category: 1=底层研发, 2=算法模型, 3=数据, 4=产品应用, ...
cat_map = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}

conn = sqlite3.connect(db_path)
c = conn.cursor()

# 查已有 jobs
c.execute("SELECT name FROM jobs WHERE is_deleted=0")
existing = {row[0] for row in c.fetchall()}
print(f'DB现有岗位: {len(existing)}')

import datetime
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

inserted = 0
for n in job_nodes:
    name = n['name']
    if name in existing:
        print(f'  已存在: {name}')
        continue
    cat_idx = n.get('category', 1)
    cat_id = cat_map.get(cat_idx, 2)
    c.execute("""
        INSERT INTO jobs (name, code, category_id, is_new, status, data_source, confidence_score, is_deleted, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
    """, (name, name.replace(' ', '_'), cat_id, 0, 'active', 'graph_import', 1.0, now, now))
    inserted += 1
    print(f'  新增: {name} (category_id={cat_id})')

if inserted:
    conn.commit()
    print(f'\n成功插入 {inserted} 个岗位到 jobs 表')
else:
    print('\n没有新岗位需要插入')

c.execute("SELECT COUNT(*) FROM jobs WHERE is_deleted=0")
total = c.fetchone()[0]
print(f'DB总岗位数: {total}')
conn.close()
