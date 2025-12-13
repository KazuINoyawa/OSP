import requests

API_BASE = 'http://localhost:8000'
TOKEN = 'dev-token'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

payload = {'title': 'Auto Created Assignment', 'description': 'Test create from script', 'due_date': '2025-12-31T23:59:00', 'class_id': 1}
print('Creating assignment...', payload)
res = requests.post(API_BASE + '/assignments', json=payload, headers=HEADERS)
print('Status', res.status_code)
try:
    print(res.json())
except Exception as e:
    print('No JSON body:', e)

res2 = requests.get(API_BASE + '/assignments')
print('Total assignments', len(res2.json()))
