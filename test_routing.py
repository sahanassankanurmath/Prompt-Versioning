"""
Run this file directly to sanity-check the router in isolation:
    python app/test_routing.py
Confirms two things:
  1. The split is close to 50/50 across many fake sessions.
  2. The same session_id always lands in the same bucket (stickiness).
"""
from routing import assign_version

if __name__ == "__main__":
    counts = {"A": 0, "B": 0}
    for i in range(10000):
        result = assign_version(session_id=f"user_{i}", experiment_id=1)
        counts[result] += 1
    print(f"Split over 10,000 sessions: {counts}")

    first_call = assign_version("user_42", experiment_id = 1)
    second_call = assign_version("user_42", experiment_id = 1)
    assert first_call == second_call, "FAILED: same session got different versions!"
    print(f"Stickiness check passed: user_42 -> {first_call} both times")