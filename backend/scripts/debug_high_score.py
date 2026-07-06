"""查看高分关联"""
import requests
d = requests.get('http://localhost:8000/api/v1/capabilities/?limit=200').json()
high = [i for i in d['items'] if (i['importance_score'] or 0) > 0.7]
print(f'High score (>0.7) associations: {len(high)}')
for i in high:
    print(f'  {i["job_name"]} -> {i["skill_name"]} (score={i["importance_score"]})')
