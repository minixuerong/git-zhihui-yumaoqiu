"""调试：查看 jobs API 返回的匹配情况"""
import urllib.request
import json

r = urllib.request.urlopen('http://localhost:8000/api/v1/jobs/?limit=500&skip=0')
d = json.loads(r.read())
print(f'总岗位数: {d["total"]}, 返回: {len(d["items"])}')

graph_names = ['AI算法工程师', '算法工程师', '智能驾驶算法工程师', 'CAE算法工程师',
               '人工智能工程师', 'AI算法工程师助理', '机器视觉工程师',
               '人工智能研发工程师', 'AI软件工程师']
for gn in graph_names:
    matched = [j for j in d['items'] if j['name'].strip() == gn or gn in j['name']]
    if matched:
        for m in matched:
            print(f'  找到: [{gn}] -> id={m["id"]}, name={m["name"]}')
    else:
        print(f'  未找到: [{gn}]')
