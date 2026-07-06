from dataclasses import dataclass


@dataclass
class StreamEvent:
    """
    Base class for all streaming events.
    """
    pass


@dataclass
class TokenEvent(StreamEvent):
    token: str


@dataclass
class Stats:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float


@dataclass
class CompletedEvent(StreamEvent):
    response: str
    stats: Stats