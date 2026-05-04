from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

TONE_PROMPTS = {
    "casual":  "in a friendly, casual tone (1 short sentence)",
    "premium": "in an elegant, premium-brand tone (1 short sentence)",
    "budget":  "highlighting value-for-money in a budget-friendly tone (1 short sentence)",
}

def get_gemini_explanation(current_prod: str, rec_prod: str, tone: str = "casual", context: dict = None):
    ctx_text = ""
    if context:
        ctx_text = f" It is {context.get('time_of_day','')} during {context.get('season','')} season."
    style = TONE_PROMPTS.get(tone, TONE_PROMPTS["casual"])
    prompt = (
        f"A user is viewing '{current_prod}'.{ctx_text} "
        f"Explain {style} why we recommend '{rec_prod}' to them. "
        f"Do NOT start with 'Because' twice. Keep under 25 words."
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print("Gemini Error:", e)
        return f"Pairs well with {current_prod} based on similar features."