import json, urllib.request

BASE = 'http://127.0.0.1:8000'

def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, ''

print('login', call('POST', '/api/v1/auth/login', {'email': 'director@company.com', 'password': 'director123'})[0])
for name, path in [('projects', '/api/v1/projects'), ('activities', '/api/v1/documents/activities'),
                   ('kpi', '/api/v1/documents/kpi-summary'), ('alerts', '/api/v1/alerts/audit')]:
    print(name, call('GET', path)[0])
print('hardware', call('POST', '/api/agent/hardware', {})[0])
print('ui has live layer:', 'LIVE DATA LAYER' in call('GET', '/')[1])
