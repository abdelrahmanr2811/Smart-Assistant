import json, requests
B = "http://127.0.0.1:8000/api/v1"
out = {}
for path in ["/projects", "/projects/active", "/documents/activities", "/documents/kpi-summary",
             "/alerts/audit", "/portfolio/summary", "/documents/s-curve", "/finance/cash-flow",
             "/claims", "/claims/variations", "/finance/ipcs", "/integrations/status", "/documents/list"]:
    try:
        r = requests.get(B + path, timeout=30)
        body = r.json()
        if isinstance(body, list):
            body = {"_len": len(body), "_first": body[:2]}
        out[path] = {"status": r.status_code, "body": body}
    except Exception as e:
        out[path] = {"error": str(e)}
with open("h:/smart assistant/backend/api_shapes.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=str)
print("ok")
