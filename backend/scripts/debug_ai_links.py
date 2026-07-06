"""检查AI算法工程师在图谱中的关联"""
import requests
r = requests.get('http://localhost:8000/api/v1/graph/data')
links = r.json()['links']
ai_links = [l for l in links if l['jobName'] == 'AI算法工程师']
print(f'AI算法工程师 links in graph: {len(ai_links)}')
for l in ai_links:
    print(f'  {l["source"]} -> {l["target"]} (val={l["value"]})')
