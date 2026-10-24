# 🤖 AI Customer Support Bot (روبوت خدمة العملاء الذكي)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-Flash-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An intelligent, production-ready AI Customer Support & Automated Inquiries Assistant powered by **Google Gemini LLM** and **FastAPI**. Designed for e-commerce stores, SaaS platforms, and enterprise service desks with native support for **Arabic (Dialects & Modern Standard Arabic)** and **English**.

روبوت محادثة ذكي ومساعد آلي لخدمة العملاء مدعوم بالذكاء الاصطناعي ونماذج Gemini، يدعم اللغة العربية واللهجات والإنجليزية بكفاءة فائقة، مع قاعدة معارف ديناميكية وتوجيه ذكي للمحادثات.

---

## 🌟 Key Features (المميزات الرئيسية)

- 🗣️ **Multilingual & Dialect Adaptive**: Understands Modern Standard Arabic (الفصحى), Egyptian & Gulf dialects, and English.
- 🎯 **Intent Recognition**: Automatically categorizes customer intent (Product Inquiry, Pricing, Order Tracking, Complaints, Human Escalation).
- 📚 **Knowledge Base & FAQ Retrieval**: Instant, accurate grounded answers based on verified product catalog and store policies.
- 👨‍💼 **Smart Human Handoff**: Automatically detects frustrated customers or complex inquiries and routes them to human support agents.
- 📊 **Real-time Analytics**: Tracks conversation volume, sentiment, common inquiries, and resolution rates.
- ⚡ **High Performance & Lightweight**: Async RESTful architecture built with FastAPI, ready for WhatsApp Business API, Telegram, or Web integration.

---

## 🏛️ System Architecture

```text
┌──────────────────────┐
│  Client (Web / Chat) │
└──────────┬───────────┘
           │ HTTPS / REST
           ▼
┌──────────────────────────────────────┐
│        FastAPI Gateway Engine        │
│  - Input Validation & Rate Limiting  │
│  - Session & Context Management      │
└──────────┬───────────────────────────┘
           │
     ┌─────┴───────────────┐
     ▼                     ▼
┌──────────────┐     ┌───────────────────────┐
│ Intent / FAQ │     │   Gemini Flash LLM    │
│ Rule Matcher │     │  Grounded AI Agent    │
└──────┬───────┘     └─────────┬─────────────┘
       │                       │
       └───────────┬───────────┘
                   ▼
     ┌───────────────────────────┐
     │  SQLite / Persistent Store│
     │  - Chat Sessions & Logs   │
     │  - Support Tickets        │
     └───────────────────────────┘
```

---

## 🚀 Quick Start (التشغيل السريع)

### 1. Clone the repository
```bash
git clone https://github.com/abdelrahmanr2811/AI-Customer-Support-Bot.git
cd AI-Customer-Support-Bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file or export your Gemini API Key:
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

### 4. Run the API Server
```bash
python main.py
```
Server runs at `http://localhost:8000`  
Interactive Swagger API documentation: `http://localhost:8000/docs`

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/chat/message` | Process customer message & return AI response |
| `GET` | `/api/v1/faq` | Retrieve all verified store FAQs |
| `POST` | `/api/v1/faq` | Add new knowledge base question/answer |
| `GET` | `/api/v1/analytics/overview` | Customer satisfaction & resolution metrics |
| `GET` | `/health` | Service health status check |

---

## 👤 Author
Developed with ❤️ by **Abdelrahman Ramadan**  
- GitHub: [@abdelrahmanr2811](https://github.com/abdelrahmanr2811)
