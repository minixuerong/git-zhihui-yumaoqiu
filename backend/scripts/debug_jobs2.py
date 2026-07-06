"""调试：查看 jobs API 返回数据"""
import urllib.request
import json

try:
    r = urllib.request.urlopen('http://localhost:8000/api/v1/jobs/?limit=500&skip=0')
    d = json.loads(r.read())
    print(f'总岗位数: {d["total"]}')
    print(f'返回条数: {len(d["items"])}')
    for item in d['items'][:15]:
        print(f'  id={item["id"]}, name={item["name"]}')
except Exception as e:
    print(f'请求失败: {e}')
