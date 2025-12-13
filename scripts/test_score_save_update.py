import requests

API_BASE = 'http://localhost:8000'
TOKEN = 'dev-token'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# Create score
payload = {'user_id': 9999, 'assignment_id': 8888, 'score': 7.5, 'feedback': 'Initial test'}
print('Creating score:', payload)
res = requests.post(f'{API_BASE}/scores', json=payload, headers=HEADERS)
print('Status:', res.status_code)
print('Response:', res.json())
created = res.json()
score_id = created.get('id')

# Update score
payload_update = {'user_id': 9999, 'assignment_id': 8888, 'score': 9.25, 'feedback': 'Updated to 9.25'}
print('\nUpdating score to:', payload_update)
res2 = requests.put(f'{API_BASE}/scores/{score_id}', json=payload_update, headers=HEADERS)
print('Status:', res2.status_code)
print('Response:', res2.json())

# Fetch all scores and find ours
res3 = requests.get(f'{API_BASE}/scores')
print('\nAll scores count:', len(res3.json()))
found = [s for s in res3.json() if s['id'] == score_id]
print('Found:', found)

if found:
    print('Stored score value:', found[0]['score'])
else:
    print('Score not found')
