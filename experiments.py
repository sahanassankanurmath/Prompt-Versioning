from db.connection import get_connection


def create_experiment(prompt_id: int, version_a_id: int, version_b_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO experiments (prompt_id, version_a_id, version_b_id)
           VALUES (%s, %s, %s)""",
        (prompt_id, version_a_id, version_b_id),
    )
    conn.commit()
    exp_id = cur.lastrowid
    cur.close()
    conn.close()
    return exp_id


def list_experiments() -> list[dict]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM experiments ORDER BY started_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def log_result(experiment_id: int, version_id: int, session_id: str,
                input_text: str, output_text: str, latency_ms: int,
                token_count: int, score: float) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO results
           (experiment_id, version_id, session_id, input_text, output_text,
            latency_ms, token_count, score)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (experiment_id, version_id, session_id, input_text, output_text,
         latency_ms, token_count, score),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_results(experiment_id: int) -> list[dict]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM results WHERE experiment_id=%s", (experiment_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows