# app/database.py

import sqlite3
import uuid

from datetime import datetime

from app.config import DATABASE_PATH


class Database:

    def __init__(self):
        """
        Connect to SQLite database.
        """

        self.connection = sqlite3.connect(DATABASE_PATH)

        self.cursor = self.connection.cursor()

        self.connection = sqlite3.connect(DATABASE_PATH)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

        self.create_tables()

    
    def create_tables(self):
        """
        Create required tables.
        """

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions(

                session_id TEXT PRIMARY KEY,

                created_at TEXT

                summary TEXT

            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                session_id TEXT,

                role TEXT,

                content TEXT,

                timestamp TEXT,

                FOREIGN KEY(session_id)
                REFERENCES sessions(session_id)

            )
            """
        )

        self.connection.commit()

    def create_session(self):

        session_id = str(uuid.uuid4())

        timestamp = datetime.now().isoformat()

        self.cursor.execute(

            """

            INSERT INTO sessions

            VALUES (?,?)

            """,

            (

                session_id,

                timestamp

            )

        )

        self.connection.commit()

        return session_id
    
    
    def save_message(self, session_id, role, content):

        timestamp = datetime.now().isoformat()

        self.cursor.execute(

            """

            INSERT INTO messages(

                session_id,

                role,

                content,

                timestamp

            )

            VALUES(?,?,?,?)

            """,

            (

                session_id,

                role,

                content,

                timestamp

            )

        )

        self.connection.commit()

    
    def load_messages(self, session_id):

        self.cursor.execute(

            """

            SELECT role,

                content

            FROM messages

            WHERE session_id=?

            ORDER BY id

            """,

            (

                session_id,

            )

        )

        rows = self.cursor.fetchall()

        messages = []

        for role, content in rows:

            messages.append(

                {

                    "role": role,

                    "content": content

                }

            )

        return messages
    
    def list_sessions(self):

        self.cursor.execute(

            """

            SELECT *

            FROM sessions

            ORDER BY created_at DESC

            """

        )

        return self.cursor.fetchall()
    
    
    def delete_session(self, session_id):

        self.cursor.execute(

            """

            DELETE

            FROM messages

            WHERE session_id=?

            """,

            (

                session_id,

            )

        )

        self.cursor.execute(

            """

            DELETE

            FROM sessions

            WHERE session_id=?

            """,

            (

                session_id,

            )

        )

        self.connection.commit()

    def save_summary(self, session_id, summary):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE sessions
            SET summary = ?
            WHERE id = ?
            """,
            (
                summary,
                session_id
            )
        )

        self.connection.commit()

    def load_summary(self, session_id):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT summary
            FROM sessions
            WHERE id = ?
            """,
            (
                session_id,
            )
        )

        row = cursor.fetchone()

        if row:
            return row["summary"]

        return None

    
    def close(self):
        self.connection.close()