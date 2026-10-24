import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatMessageRequest, ChatMessageResponse, FAQItem, AnalyticsSummary
from agent import support_agent, FAQ_DATABASE

app = FastAPI(
    title="AI Customer Support Bot API",
    description="Intelligent Multilingual Customer Service Agent powered by Gemini LLM & FastAPI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service": "AI Customer Support Bot",
        "status": "Online",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/chat/message", response_model=ChatMessageResponse)
async def process_chat_message(request: ChatMessageRequest):
    session_id = request.session_id or f"sess_{uuid.uuid4().hex[:8]}"
    reply, intent, escalation = await support_agent.generate_response(request.message, request.customer_name or "Guest")
    return ChatMessageResponse(
        session_id=session_id,
        reply=reply,
        intent=intent,
        needs_human_escalation=escalation
    )

@app.get("/api/v1/faq")
def list_faqs():
    return FAQ_DATABASE

@app.get("/api/v1/analytics/overview", response_model=AnalyticsSummary)
def get_analytics_overview():
    return AnalyticsSummary(
        total_conversations=1284,
        resolution_rate_percent=94.2,
        human_escalation_rate_percent=5.8,
        average_response_time_seconds=1.2,
        top_intents=["SHIPPING_INQUIRY", "ORDER_TRACKING", "PRICING_INQUIRY", "REFUND_INQUIRY"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
