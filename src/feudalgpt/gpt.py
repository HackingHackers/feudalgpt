from dataclasses import dataclass
import json
from typing import List, Union
from llama_cpp import Llama, CreateChatCompletionResponse, CreateChatCompletionStreamResponse

@dataclass
class GPTMessage:
    """A message in the conversation between GPTs."""
    role: str
    message: str

class GPT:
    """A GPT model that can participate in a conversation."""
    name: str
    role: str
    messageQueue: list[GPTMessage]
    model: Llama
    def __init__(self, name: str, role: str, llm: Llama):
        self.name = name
        self.role = role
        self.messageQueue = []
        self.model = llm

if __name__ == "__main__":
    import os
    # test Llama
    llm = Llama.from_pretrained(
        repo_id="Qwen/Qwen1.5-7B-Chat-GGUF",
        filename="*q4_0.gguf",
        verbose=False
    )
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are my best friend."},
            {"role": "user", "content": "From now on, you are a young white teenage boy."},
        ],
        temperature=0.7,
    )
    print(json.dumps(output))

    # Test GPT class
    gpt = GPT("Qwen1.5-7B-Chat-GGUF", "boss", llm)
    this_path = os.path.dirname(os.path.realpath(__file__))
    prompt = open(os.path.join(this_path, "prompts", "common.txt"), "r").read()
    print(gpt.model.create_chat_completion(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Please write \'Hello, World\' to the 3rd line of the notebook."},
        ],
        temperature=0.7,
    ))
