"""
FarmSphere — AI Chatbot
Uses Google Gemini API. Falls back to keyword-based responses if key missing.
"""
import os


SYSTEM_PROMPT = """You are FarmBot, an expert AI farming assistant for FarmSphere.
You specialise in: crop diseases & treatment, fertilizer recommendations, irrigation,
pest management, soil health, weather impact, market prices, and organic farming.
Keep answers concise (2–4 paragraphs), practical, and farmer-friendly.
When the user writes in Hindi or Marathi, reply in the same language."""


class FarmSphereChatbot:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self._model = None
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel(
                    "gemini-pro",
                    system_instruction=SYSTEM_PROMPT,
                )
            except Exception:
                self._model = None

    def chat(self, message: str, history: list = None) -> str:
        """Send a message and return the AI reply."""
        if self._model:
            try:
                chat_history = []
                for h in (history or [])[-10:]:
                    role = h.get("role", "user")
                    content = h.get("content", "")
                    if role in ("user", "assistant") and content:
                        chat_history.append({
                            "role": "model" if role == "assistant" else "user",
                            "parts": [content],
                        })
                session = self._model.start_chat(history=chat_history)
                return session.send_message(message).text
            except Exception:
                pass
        return self.get_fallback_response(message)

    # ------------------------------------------------------------------ #
    # Fallback keyword responses — used when no API key is configured
    # ------------------------------------------------------------------ #
    def get_fallback_response(self, message: str) -> str:
        ml = message.lower()

        if any(w in ml for w in ["blight", "rust", "mildew", "spot", "wilt", "disease", "leaf", "fungus"]):
            return (
                "🌿 **Disease Advisory**\n\n"
                "Common fungal/bacterial infections spread in humid conditions.\n\n"
                "**Immediate steps:** Remove infected leaves → Apply copper-based fungicide (Bordeaux mixture) "
                "→ Improve air circulation → Avoid overhead watering.\n\n"
                "Upload a leaf photo to our **Disease Diagnosis** page for precise AI identification and "
                "crop-specific treatment recommendations."
            )

        if any(w in ml for w in ["fertilizer", "npk", "urea", "dap", "nutrient", "nitrogen", "potassium"]):
            return (
                "🌱 **Fertilizer Guide**\n\n"
                "Always start with a soil test to identify deficiencies.\n\n"
                "**General NPK for Kharif cereals:** N:120 | P:60 | K:40 kg/ha\n"
                "**For Rabi wheat:** Basal 60:60:40 + top-dress 60kg N at CRI stage.\n\n"
                "Add organic compost (5–10 t/ha) to improve soil structure and microbial activity. "
                "Micronutrient spray (Zn 0.5%) boosts yield by 8–12%."
            )

        if any(w in ml for w in ["irrigation", "water", "drip", "sprinkler", "flood"]):
            return (
                "💧 **Irrigation Advisory**\n\n"
                "Drip irrigation saves 35–45% water vs. flood method and reduces disease pressure.\n\n"
                "**Best practice:** Water early morning to minimise evaporation → "
                "Use tensiometers to monitor soil moisture → "
                "Critical stages for irrigation: germination, flowering, grain filling.\n\n"
                "Check our **Weather** page for rain forecasts before scheduling irrigation."
            )

        if any(w in ml for w in ["pest", "insect", "aphid", "thrip", "whitefly", "bollworm", "caterpillar"]):
            return (
                "🐛 **Pest Management (IPM)**\n\n"
                "Integrated Pest Management combines biological, cultural, and chemical controls.\n\n"
                "**Step 1:** Scout fields every 7 days and note Economic Threshold Level (ETL).\n"
                "**Step 2:** Use sticky yellow/blue traps for monitoring.\n"
                "**Step 3:** Release natural predators (Trichogramma, Chrysoperla).\n"
                "**Step 4:** If above ETL, spray neem-based pesticide or selective insecticide.\n\n"
                "Avoid broad-spectrum pesticides during flowering to protect pollinators."
            )

        if any(w in ml for w in ["price", "market", "msp", "mandi", "sell", "profit"]):
            return (
                "💰 **Market Intelligence**\n\n"
                "Strategic timing of your sale can increase profit by 15–25%.\n\n"
                "**Tips:** Monitor daily APMC mandi rates → Sell when price is 10%+ above MSP → "
                "Consider Farmer Producer Organisations (FPO) for collective bargaining → "
                "Use e-NAM platform for direct online market access.\n\n"
                "Use our **Price Prediction** tool for AI-powered monthly forecasts."
            )

        if any(w in ml for w in ["weather", "rain", "drought", "flood", "temperature", "humidity"]):
            return (
                "🌦️ **Weather & Farm Planning**\n\n"
                "Always check 7-day forecasts before spraying, transplanting, or harvesting.\n\n"
                "**High humidity (>80%):** Increases fungal risk — apply preventive fungicide.\n"
                "**Temperatures above 38°C:** Increase irrigation frequency and apply mulch.\n"
                "**Heavy rain forecast:** Delay fertilizer application by 48 hours.\n\n"
                "Visit our **Weather** page for real-time local forecasts and farming alerts."
            )

        if any(w in ml for w in ["soil", "ph", "organic", "compost", "carbon", "microbe"]):
            return (
                "🌍 **Soil Health**\n\n"
                "Healthy soil = 45% minerals, 25% water, 25% air, 5% organic matter.\n\n"
                "**Improvement steps:** Conduct soil test every 2–3 years → "
                "Maintain pH 6.0–7.5 for most crops → "
                "Add farmyard manure (FYM) 10–15 t/ha → "
                "Practice green manuring with dhaincha or sunhemp → "
                "Minimise tillage to preserve soil structure.\n\n"
                "Biofertilizers (Rhizobium, Azotobacter) can fix 20–30 kg N/ha naturally."
            )

        # Generic welcome
        return (
            "🚜 **FarmBot — AI Farming Assistant**\n\n"
            "Hello! I'm your 24/7 farming expert. I can help with:\n\n"
            "🌿 Crop disease diagnosis & treatment\n"
            "💧 Irrigation planning & scheduling\n"
            "🌱 Fertilizer & soil nutrition advice\n"
            "🐛 Pest & weed management (IPM)\n"
            "💰 Market prices & selling strategy\n"
            "🌦️ Weather impact on crop management\n\n"
            "Ask me anything, or use the modules above for AI-powered analysis. "
            "*(Add your GEMINI_API_KEY in .env for full conversational AI)*"
        )
