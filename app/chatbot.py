from rich.console import Console
from rich.status import Status

from app.config import (
    client,
    MODEL_NAME,
)

console = Console()

class ChatBot:

    def __init__(self):
        self.client = client
        self.model = MODEL_NAME

    def stream_response(self, messages):

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )

        with console.status("[bold green]Thinking..."):
            first_chunk = next(stream)

        response = ""

        token = first_chunk.choices[0].delta.content

        if token:
            console.print(token, end="")
            response += token
        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                console.print(token, end="")
                response += token
        console.print()
        return response