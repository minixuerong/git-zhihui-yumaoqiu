"""检查AI算法工程师的关联情况"""
import requests

# 检查 graph/jobs 返回的 ID
r = requests.get('http://localhost:8000/api/v1/graph/jobs')
for j in r.json():
    if 'AI算法工程师' in j['name']:
        print(f'Graph jobs API: id={j["id"]}, name="{j["name"]}", db_name="{j["db_name"]}"')

# 检查 capability_requirements 中 AI算法工程师的关联
r2 = requests.get('http://localhost:8000/api/v1/capabilities/?limit=200')
ai_links = [i for i in r2.json()['items'] if 'AI算法工程师' in i.get('job_name', '')]
print(f'\nAI算法工程师 capability_requirements: {len(ai_links)}')
for l in ai_links[:5]:
    print(f'  job_id={l["job_id"]}, skill_id={l["skill_id"]}, skill={l["skill_name"]}, score={l["importance_score"]}')

# Check graph_data for AI算法工程师 links
r3 = requests.get('http://localhost:8000/api/v1/graph/data')
links = r3.json()['links']
ai_graph_links = [l for l in links if 'AI算法工程师' in l.get('source', '') or 'AI算法工程师' in l.get('jobName', '')]
print(f'\nGraph links for AI算法工程师: {len(ai_graph_links)}')
for l in ai_graph_links[:5]:
    print(f'  {l["source"]} -> {l["target"]} (value={l["value"]})')
