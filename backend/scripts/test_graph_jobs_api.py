import requests
r = requests.get('http://localhost:8000/api/v1/graph/jobs')
print(f'Status: {r.status_code}')
print(f'Count: {len(r.json())}')
for j in r.json():
    print(f'  id={j["id"]}, name="{j["name"]}", db_name="{j["db_name"]}"')
