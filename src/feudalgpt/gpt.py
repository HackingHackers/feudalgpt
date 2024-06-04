from dataclasses import dataclass

@dataclass
class GPTMessage:
    role: str
    message: str

class GPT:
    name: str
    role: str
    messageQueue: list[GPTMessage]