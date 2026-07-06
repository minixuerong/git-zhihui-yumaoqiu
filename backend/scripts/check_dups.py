"""检查API返回的节点是否有重复id"""
import urllib.request
import json
from collections import Counter

r = urllib.request.urlopen('http://localhost:8000/api/v1/graph/data')
d = json.loads(r.read())

# 检查重复的 id（ECharts 用 id 识别节点）
ids = [n['id'] for n in d['nodes']]
dups = {n: c for n, c in Counter(ids).items() if c > 1}
if dups:
    print(f'重复的节点 id: {dups}')
else:
    print('✅ 没有重复节点 id')

# 检查 sample
print(f'总节点: {len(d["nodes"])}')
print(f'总边: {len(d["links"])}')
print(f'\n前3个节点 sample:')
for n in d['nodes'][:3]:
    print(f'  id={n["id"]}, name={n["name"]}, cat={n["category"]}')
print(f'\n前3条边 sample:')
for l in d['links'][:3]:
    print(f'  source={l["source"]}, target={l["target"]}, val={l["value"]}')
