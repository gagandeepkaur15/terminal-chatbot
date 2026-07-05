from app.database import Database
from app.config import SUMMARY_TRIGGER, WINDOW_SIZE


class MemoryManager:

    def __init__(self):
        self.db = Database()
        self.session_id = self.db.create_session()

        # Cache conversation in memory for fast access
        self.messages = []

        # Long-term memory summary stored as a system message
        self.summary_message = None

    def add_message(self, role, content):
        message = {
            "role": role,
            "content": content
        }

        self.messages.append(message)

        self.db.save_message(
            self.session_id,
            role,
            content
        )

    def get_messages(self):
        return self.messages

    def load_session(self, session_id):
        self.session_id = session_id

        self.messages = self.db.load_messages(
            session_id
        )

    def new_session(self):
        self.session_id = self.db.create_session()
        self.messages = []
        self.summary_message = None

    def get_session_id(self):
        return self.session_id

    def get_recent_messages(self):
        if len(self.messages) <= WINDOW_SIZE:
            return self.messages

        return self.messages[-WINDOW_SIZE:]

    def build_conversation(self, system_prompt):

        conversation = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Add long-term memory summary if available
        if self.summary_message is not None:
            conversation.append(self.summary_message)

        # Add recent conversation
        conversation.extend(
            self.get_recent_messages()
        )

        return conversation

    def compress_memory(self, chatbot):

        if len(self.messages) <= SUMMARY_TRIGGER:
            return

        messages_to_summarize = self.messages[:-WINDOW_SIZE]
        recent_messages = self.messages[-WINDOW_SIZE:]

        summary_prompt = [
            {
                "role": "system",
                "content": (
                    "You are a conversation memory manager.\n\n"

                    "Maintain ONE concise long-term memory "
                    "summary of the conversation.\n\n"

                    "Preserve:\n"
                    "- User identity\n"
                    "- Preferences\n"
                    "- Goals\n"
                    "- Ongoing tasks\n"
                    "- Important facts\n"
                    "- Decisions\n\n"

                    "Remove:\n"
                    "- Greetings\n"
                    "- Small talk\n"
                    "- Duplicate information\n"
                    "- Temporary discussions\n\n"

                    "Return ONLY the updated summary."
                )
            }
        ]

        # Give the model the previous summary
        if self.summary_message is not None:

            summary_prompt.append(
                {
                    "role": "system",
                    "content":
                        "Current Memory Summary:\n\n"
                        + self.summary_message["content"]
                }
            )

        summary_prompt.append(
            {
                "role": "user",
                "content":
                    "Update the memory summary using the following conversation."
            }
        )

        summary_prompt.extend(
            messages_to_summarize
        )

        updated_summary = chatbot.generate(
            summary_prompt
        )

        # Replace the previous summary with the new one
        self.summary_message = {
            "role": "system",
            "content": f"Conversation Summary:\n{updated_summary}"
        }

        # Keep only the recent messages in RAM
        self.messages = recent_messages

    def close(self):
        self.db.close()