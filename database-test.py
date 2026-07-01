from app.database import Database

db = Database()

session_id = db.create_session()

print("Session:", session_id)

db.save_message(
    session_id,
    "user",
    "Hello"
)

db.save_message(
    session_id,
    "assistant",
    "Hi! How are you?"
)

messages = db.load_messages(session_id)

print(messages)

print(db.list_sessions())

db.close()