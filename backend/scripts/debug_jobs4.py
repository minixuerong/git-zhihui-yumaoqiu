"""调试 jobs API 返回的图谱岗位"""
import requests

r = requests.get('http://localhost:8000/api/v1/jobs/?limit=500')
data = r.json()
items = data.get('items', [])
print(f'Total items from API: {len(items)}')

names = ['AI算法工程师', '算法工程师', '智能驾驶算法工程师', 'CAE算法工程师',
         '人工智能工程师', 'AI算法工程师助理', '机器视觉工程师',
         '人工智能研发工程师', 'AI软件工程师']

for n in names:
    found = [j for j in items if j['name'].strip().lower() == n.lower()]
    if found:
        print(f'  OK: id={found[0]["id"]}, name="{found[0]["name"]}"')
    else:
        print(f'  MISSING: {n}')
        # Try partial match
        partial = [j for j in items if n.lower() in j['name'].lower()]
        if partial:
            print(f'    (partials: {[p["name"] for p in partial[:3]]})')
