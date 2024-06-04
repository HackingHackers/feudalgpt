from feudalgpt.gpt import GPT


class Environment:
    note: list[str]
    gpts: map[str, GPT]
