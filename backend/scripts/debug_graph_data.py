"""检查图谱数据和 capability_requirements"""
import requests

# 1. 检查 capability_requirements 有多少条
r = requests.get('http://localhost:8000/api/v1/capabilities/?limit=200')
data = r.json()
print(f'Capability requirements total: {data["total"]}')
print(f'Capability requirements items: {len(data["items"])}')
if data["items"]:
    for item in data["items"][:5]:
        print(f'  job={item["job_name"]}, skill={item["skill_name"]}, score={item["importance_score"]}')
    # Check scores distribution
    scores = [i["importance_score"] or 0 for i in data["items"]]
    print(f'  Scores range: {min(scores):.1f} - {max(scores):.1f}, avg={sum(scores)/len(scores):.2f}')

# 2. 检查图谱数据
r2 = requests.get('http://localhost:8000/api/v1/graph/data')
gd = r2.json()
print(f'\nGraph nodes: {len(gd["nodes"])}')
print(f'Graph links: {len(gd["links"])}')
if gd["links"]:
    for l in gd["links"][:5]:
        print(f'  {l["source"]} -> {l["target"]} (value={l["value"]})')
