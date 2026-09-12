import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model = genai.GenerativeModel("gemini-1.5-flash")


def run_prompt_version(prompt_template: str, user_input: str) -> dict:
    """
    Calls the LLM with a filled-in prompt and returns output + metrics.
    prompt_template must contain '{input}' as a placeholder.
    """
    filled_prompt = prompt_template.format(input=user_input)
    start = time.time()
    try:
        response = _model.generate_content(filled_prompt)
        latency_ms = int((time.time() - start) * 1000)
        return {
            "output": response.text,
            "latency_ms": latency_ms,
            "token_count": response.usage_metadata.total_token_count,
            "error": None,
        }
    except Exception as e:
        # Never let a bad API call crash the whole experiment - log it as a failed result instead
        return {
            "output": "",
            "latency_ms": int((time.time() - start) * 1000),
            "token_count": 0,
            "error": str(e),
        }