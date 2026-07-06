from urllib import response

from rich.console import Console

from app.config import (
    client,
    MODEL_NAME,
)
from app.events import CompletedEvent, Stats, TokenEvent
from app.tokenizer import TokenCounter

console = Console()

class ChatBot:

    def __init__(self):
        self.client = client
        self.model = MODEL_NAME
        self.token_counter = TokenCounter()

    def generate(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

    def stream_response(self, messages):
        """
        Streams the response from Groq and returns:
        1. Complete response text
        2. Token & cost statistics
        """

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )

        response = ""

        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                response += token

                # Yield each token to the caller so that it can be displayed in real-time one token at a time instead of waiting for the entire response to be generated
                yield TokenEvent(token)

        # ----------------------------
        # Token counting
        # ----------------------------

        prompt_tokens = self.token_counter.count_messages(
            messages
        )

        completion_tokens = self.token_counter.count(
            response
        )

        cost = self.token_counter.calculate_cost(
            prompt_tokens,
            completion_tokens
        )

        stats = Stats(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,

            input_cost=cost["input"],
            output_cost=cost["output"],
            total_cost=cost["total"]
        )

        yield CompletedEvent(
            response=response,
            stats=stats
        )