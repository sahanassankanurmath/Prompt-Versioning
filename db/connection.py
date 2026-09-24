import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def get_connection():
    required_settings = ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME")
    missing_settings = [name for name in required_settings if not os.getenv(name)]
    if missing_settings:
        missing = ", ".join(missing_settings)
        raise RuntimeError(
            f"Missing database settings: {missing}. "
            "Create a .env file in the project root using .env.example."
        )

    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )