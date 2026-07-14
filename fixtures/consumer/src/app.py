"""Simple web application for testing security review skills."""

import os
import sqlite3


def get_user(user_id: int) -> dict:
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return {}
    return {"id": row[0], "name": row[1], "email": row[2]}


def list_files(directory: str) -> list[str]:
    safe_path = os.path.normpath(directory)
    if ".." in safe_path or safe_path.startswith("/"):
        raise ValueError("Invalid path")
    return os.listdir(safe_path)


def health_check() -> dict:
    return {"status": "ok"}
