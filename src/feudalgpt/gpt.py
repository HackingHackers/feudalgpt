from dataclasses import dataclass


@dataclass
class GPTMessage:
    role: str
    message: str

class GPT:
    name: str
    role: str
    messageQueue: list[GPTMessage]
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.messageQueue = []
