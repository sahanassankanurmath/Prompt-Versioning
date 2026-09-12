from db.connection import get_connection

def create_prompt(name:str) -> int:
    """Creates a new prompt in the database and returns its ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO prompts (name) VALUES (%s)", (name,))
    conn.commit()
    prompt_id = cur.lastrowid
    cur.close()
    conn.close()
    return prompt_id

def create_new_version(prompt_id: int, content: str, note: str = "") -> int:
    """Inserts a new immutable version. Never edits an existing version row."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "Select coalesce(MAX(version_number), 0) from prompt_versions where prompt_id = %s",
        (prompt_id,),
    )
    next_version = cur.fetchone()[0] + 1
    cur.execute(
        """Insert into prompt_versions (prompt_id, version_number, content, change_note)
        values (%s,%s,%s,%s)""",
        (prompt_id, next_version, content, note),
    )
    conn.commit()
    version_id = cur.lastrowid
    cur.close()     
    conn.close()
    return version_id

def list_prompts() -> list[dict]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("Select * from prompts order by created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def list_versions(prompt_id: int) -> list[dict]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "Select * from prompt_versions where prompt_id = %s order by version_number DESC",
        (prompt_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows