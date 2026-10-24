import os
import re
import uuid
from typing import Dict, Any, Tuple
import requests

FAQ_DATABASE = [
    {
        "keywords": ["شحن", "توصيل", "shipping", "delivery"],
        "answer": "يتم التوصيل خلال 2 إلى 4 أيام عمل لكافة المحافظات والمناطق. الشحن مجاني للطلبات التي تتجاوز 500 جنيه/ريال."
    },
    {
        "keywords": ["استرجاع", "استبدال", "return", "refund", "exchange"],
        "answer": "يمكنك استرجاع أو استبدال أي منتج خلال 14 يوماً من تاريخ الاستلام بشرط أن يكون المنتج بحالته الأصلية ومعه الفاتورة."
    },
    {
        "keywords": ["دفع", "فيزا", "كاش", "payment", "cod", "credit card"],
        "answer": "نوفر خيارات دفع متعددة: الدفع عند الاستلام (Cash on Delivery)، البطاقات الائتمانية (Visa / MasterCard)، والمحافظ الإلكترونية."
    },
    {
        "keywords": ["طلب", "تتبع", "track", "order status", "فين طلبي"],
        "answer": "يمكنك تتبع حالة شحنتك فوراً بإرسال رقم الطلب هنا، أو عبر رسالة التأكيد النصية المرسلة لهاتفك."
    },
    {
        "keywords": ["ضمان", "warranty", "صيانة"],
        "answer": "جميع المنتجات الأصلية مشمولة بضمان رسمي لمدة عامين ضد عيوب الصناعة مع مراكز خدمة معتمدة."
    }
]

class SupportAgent:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")

    def detect_intent(self, text: str) -> Tuple[str, bool]:
        t = text.lower()
        if any(w in t for t in ["موظف", "انسان", "بشري", "خدمة العملاء", "مشكلة", "شكوى", "نصب", "human", "agent", "escalate", "manager"]):
            return "HUMAN_ESCALATION", True
        elif any(w in t for t in ["شحن", "توصيل", "shipping", "delivery"]):
            return "SHIPPING_INQUIRY", False
        elif any(w in t for t in ["استرجاع", "استبدال", "refund", "return"]):
            return "REFUND_INQUIRY", False
        elif any(w in t for t in ["سعر", "بكام", "تكلفة", "price", "cost"]):
            return "PRICING_INQUIRY", False
        elif any(w in t for t in ["تتبع", "الطلب", "فين طلبي", "order"]):
            return "ORDER_TRACKING", False
        return "GENERAL_INQUIRY", False

    def find_faq_answer(self, text: str) -> str:
        t = text.lower()
        for item in FAQ_DATABASE:
            if any(k in t for k in item["keywords"]):
                return item["answer"]
        return ""

    async def generate_response(self, message: str, customer_name: str = "عزيزي العميل") -> Tuple[str, str, bool]:
        intent, needs_escalation = self.detect_intent(message)
        
        if needs_escalation:
            reply = (
                f"أهلاً بك {customer_name}! 👨‍💼 تم تحويل محادثتك لأحد ممثلي خدمة العملاء وسيتواصل معك خلال لحظات. "
                "إذا كان لديك رقم طلب يرجى كتابته هنا لتسريع المساعدة."
            )
            return reply, intent, True

        faq_ans = self.find_faq_answer(message)
        if faq_ans:
            return faq_ans, intent, False

        # If Gemini API Key is configured, use Gemini
        if self.gemini_api_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={self.gemini_api_key}"
                prompt = (
                    "You are a professional, friendly, and helpful AI Customer Support Representative for a premium store.\n"
                    "Respond politely, concisely, and helpfully in the same language as the customer (Arabic or English).\n\n"
                    f"Customer: {message}\n"
                    "Support Assistant:"
                )
                r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=8)
                if r.status_code == 200:
                    text_out = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return text_out, intent, False
            except Exception:
                pass

        # Intelligent Fallback
        reply = (
            f"أهلاً بك {customer_name}! يسعدنا مساعدتك في أي استفسار يخص منتجاتنا، الشحن والتوصيل، أو سياسة الاسترجاع. "
            "كيف يمكنني خدمتك اليوم؟"
        )
        return reply, intent, False

support_agent = SupportAgent()
