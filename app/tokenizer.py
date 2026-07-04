import tiktoken

from app.config import (
    INPUT_COST_PER_MILLION,
    OUTPUT_COST_PER_MILLION,
)


class TokenCounter:
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def count(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def count_messages(self, messages: list) -> int:
        total = 0

        for message in messages:
            total += self.count(message["content"])

        return total

    def calculate_cost(
        self,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> dict:

        input_cost = (
            prompt_tokens / 1_000_000
        ) * INPUT_COST_PER_MILLION

        output_cost = (
            completion_tokens / 1_000_000
        ) * OUTPUT_COST_PER_MILLION

        return {
            "input": input_cost,
            "output": output_cost,
            "total": input_cost + output_cost,
        }