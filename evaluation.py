from llm_client import _model


def score_basic(output: str) -> float:
    """Cheap heuristic score - use this first to get the pipeline working end-to-end."""
    if not output:
        return 0.0
    length_ok = 20 < len(output) < 800
    return 1.0 if length_ok else 0.0


def score_with_judge(user_input: str, output: str) -> float:
    """
    Uses the LLM itself as a grader. More expensive and slower than score_basic,
    so swap this in only once the pipeline is confirmed working end-to-end.
    """
    if not output:
        return 0.0
    judge_prompt = f"""Rate the following response from 1 to 5 for helpfulness and accuracy.
Reply with ONLY the number, nothing else.

Question: {user_input}
Response: {output}"""
    try:
        result = _model.generate_content(judge_prompt)
        return float(result.text.strip())
    except (ValueError, Exception):
        return 0.0