import sqlite3
import json


DATABASE_NAME = "research_assistant.db"


def create_database():
    """
    Create the SQLite database and research_logs table if they do not already exist.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer_json TEXT NOT NULL,
            model TEXT NOT NULL,
            prompt_tokens INTEGER NOT NULL,
            completion_tokens INTEGER NOT NULL,
            total_tokens INTEGER NOT NULL,
            estimated_cost_usd REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_question_to_database(question, answer, model, usage, estimated_cost, timestamp):
    """
    Save one question and structured answer to the SQLite database.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    answer_json = json.dumps(answer)

    cursor.execute("""
        INSERT INTO research_logs (
            question,
            answer_json,
            model,
            prompt_tokens,
            completion_tokens,
            total_tokens,
            estimated_cost_usd,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        question,
        answer_json,
        model,
        usage["prompt_tokens"],
        usage["completion_tokens"],
        usage["total_tokens"],
        estimated_cost["total_cost_usd"],
        timestamp
    ))

    connection.commit()
    connection.close()
    
def get_recent_questions(limit=5):
    """
    Get the most recent questions from the SQLite database.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            question,
            total_tokens,
            estimated_cost_usd,
            created_at
        FROM research_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return rows