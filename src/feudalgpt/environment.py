from gpt import GPT


class Environment:
    note: list[str]
    gpts: dict[str, GPT]
    def __init__(self):
        self.note = []
        self.gpts = {}
