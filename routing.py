import hashlib

def assign_version(session_id: str, experiment_id: int, split: int = 50) -> str:
      """
    Deterministically assigns a session to 'A' or 'B'.
    Same session_id + experiment_id always returns the same bucket,
    so one user doesn't flip between versions mid-experiment.
    `split` = percentage that goes to A (default 50/50).
    """
      key = f"{experiment_id}:{session_id}"
      digest = hashlib.md5(key.encode()).hexdigest()
      bucket = int(digest, 16) % 100
      return "A" if bucket < split else "B"