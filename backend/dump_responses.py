import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app.core.agent import agent_orchestrator
from app.core.database import init_db

init_db()

async def dump():
    queries = [
        ("SPI / CPI", "احسبلي مؤشرات الأداء الـ SPI والـ CPI وموقف المشروع الحالي"),
        ("QA/QC Contact", "مين مسؤول الـ QA/QC ورقم تليفونه؟"),
        ("Rebar / Concrete Log", "شوفلي سجل توريدات خرسانة اللبشة وحديد التسليح وحالة الفحص"),
        ("Email Request", "ابعت إيميل لمهندس الموقع شريف بخصوص صبة القواعد"),
        ("Small Talk", "كيفك يا باشمهندس؟ أخبارك إيه؟")
    ]
    results = {}
    for label, q in queries:
        res = await agent_orchestrator.process_message(user_message=q, session_id="sess_live_dump")
        results[label] = {
            "query": q,
            "response": res.response,
            "action_required": res.action_required.model_dump() if res.action_required else None,
            "sources": res.sources,
            "dataset": "SAMPLE_DATABASE (Initial Project Seed)"
        }
        await asyncio.sleep(6)
    
    with open("live_chat_dump.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("DUMP_SUCCESS")

if __name__ == "__main__":
    asyncio.run(dump())
