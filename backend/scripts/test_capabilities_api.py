"""测试能力需求 API - 带详细错误"""
import urllib.request
import json

try:
    req = urllib.request.Request('http://localhost:8000/api/v1/capabilities/?limit=5')
    r = urllib.request.urlopen(req)
    d = json.loads(r.read())
    print(f'能力需求列表: 共 {d["total"]} 条')
    for item in d['items'][:5]:
        print(f'  {item["job_name"]} → {item["skill_name"]} (重要度={item["importance_score"]})')
    print('\n✅ 成功')
except urllib.error.HTTPError as e:
    print(f'HTTP 错误: {e.code}')
    print(f'响应: {e.read().decode()}')
except Exception as e:
    print(f'错误: {e}')
