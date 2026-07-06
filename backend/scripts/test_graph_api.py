"""测试图谱 API"""
import urllib.request
import json

try:
    r = urllib.request.urlopen('http://localhost:8000/api/v1/graph/data')
    d = json.loads(r.read())
    print(f"分类: {len(d['categories'])}")
    print(f"节点: {len(d['nodes'])}")
    print(f"边: {len(d['links'])}")
    print(f"jobSkills 岗位数: {len(d['jobSkills'])}")
    print(f"分类统计: {len(d['categoryStats'])}")
    
    print("\n=== 前5个节点 ===")
    for n in d['nodes'][:5]:
        print(f"  {n['name']} (cat={n['category']}, size={n['symbolSize']})")
    
    print("\n=== 前5条边 ===")
    for l in d['links'][:5]:
        print(f"  {l['source']} -> {l['target']} (value={l['value']})")
        
except Exception as e:
    print(f"错误: {e}")
