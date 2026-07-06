"""打印图数据统计"""
import requests
r = requests.get('http://localhost:8000/api/v1/graph/data')
d = r.json()
print(f'Nodes: {len(d["nodes"])}, Links: {len(d["links"])}')
for l in d["links"]:
    print(f'  {l["source"]} -> {l["target"]} (val={l["value"]})')
