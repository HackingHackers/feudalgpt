# /// script
# requires-python = ">=3.9"
# ///

from environment import Environment
from gpt import GPT, GPTMessage

COMMANDS = {
    "read_text": {
        "args": ["<line-no>"],
        "multiline": False,
        "description": "Reads the text from the specified line number, <line-no>.",
    },
    "write_text": {
        "args": ["<line-no>", "<content>"],
        "multiline": True,
        "description": "Writes the text to the specified line number, <line-no>. The command is closed by '$end write_text'",
    },
    "add_line": {
        "args": ["<line-no>"],
        "multiline": False,
        "description": "Adds a new line after the given line number.",
    },
    "remove_line": {
        "args": ["<line-no>"],
        "multiline": False,
        "description": "Removes the line at the given line number.",
    },
    "tell": {
        "args": ["<name>", "<message>"],
        "multiline": True,
        "description": "Tell another GPT a message. it is closed by command '$end tell'",
    },
}

class Command:
    action: str
    args: list[str]
    def execute(self, env: Environment, gpt: GPT):
        """
        Executes the command.
        """
        if self.action == "read_text":
            linum = int(self.args[0])
            gpt.messageQueue.append(GPTMessage("system", env.read_text(linum)))
        elif self.action == "write_text":
            linum = int(self.args[0])
            text = self.args[1]
            env.write_text(linum, text)
        elif self.action == "add_line":
            linum = int(self.args[0])
            env.add_line(linum)
        elif self.action == "remove_line":
            linum = int(self.args[0])
            env.remove_line(linum)
        elif self.action == "tell":
            gpt_name = self.args[0]
            message = self.args[1]
            if gpt_name not in env.gpts:
                gpt.messageQueue.append(GPTMessage("system", f"GPT '{gpt_name}' does not exist."))
                return
            env.gpts[gpt_name].messageQueue.append(GPTMessage(gpt.name, message))

def parse(this_gpt: GPT, text: str):
    """
    Parses the text into a list of commands.
    The parser will ignore any line that does not start with a '$', if it is not inside a block command.
    The function will return the list of commands.
    """
    commands = []
    multiline_command_tmp = None
    in_multiline_command = None
    for line in text.split('\n'):
        line = line.strip()
        if in_multiline_command:
            # still inside a multiline command. Add the current line to the last argument.
            if line == f"$end {in_multiline_command}":
                in_multiline_command = None
                commands.append(multiline_command_tmp)
                continue
            multiline_command_tmp.args[-1] += line + '\n'
            continue
        else:
            # not inside a multiline command
            if line.startswith('$'):
                # marks the start of a command
                args = line[1:].split(' ')
                command = Command()
                command.action = args[0]
                command.args = args[1:]
                if command.action not in COMMANDS:
                    this_gpt.messageQueue.append(GPTMessage("system", f"Command '{command.action}' is not a valid command."))
                    continue
                if COMMANDS[command.action]["multiline"]:
                    # the command itself is a multiline command. Start a new multiline command.
                    in_multiline_command = command.action
                    multiline_command_tmp = command
                    command.args.append('')   # append an empty argument for the text below
                elif len(command.args) != len(COMMANDS[command.action]["args"]):
                    this_gpt.messageQueue.append(GPTMessage("system", f"Command '{command.action}' requires {len(COMMANDS[command.action]['args'])} arguments."))
                    continue
                else:
                    commands.append(command)
    return commands

if __name__ == "__main__":
    print("Testing command.py")
    env = Environment()
    gpt = GPT("gpt", "gpt")
    env.gpts["gpt"] = gpt
    text = """
    $read_text 1
    Some unrelated text.
    $add_line 1
    $write_text 2
    Hello, world!
    This is another line.
    $end write_text
    $remove_line 1
    $tell gpt2
    Hello, GPT2!
    If you can read this, it means the command is working.
    Please write a message to the notebook to confirm.
    Type the following command:
    $write_text 3
    I can read the message.
    $end write_text
    $end tell
    """
    commands = parse(gpt, text)
    for command in commands:
        print(command.action, command.args)