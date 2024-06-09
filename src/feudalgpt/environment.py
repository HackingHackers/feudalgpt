from gpt import GPT


class Environment:
    note: list[str]
    gpts: dict[str, GPT]
    def __init__(self):
        self.note = []
        self.gpts = {}
    def write_text(self, linum: int, text: str):
        """
        Writes the text to the specified line.
        """
        if linum > len(self.note):
            self.note += [''] * (linum - len(self.note))
        self.note[linum] = text
    def read_text(self, linum: int):
        """
        Reads the text from the specified line.
        """
        return self.note[linum]
    def add_line(self, linum: int):
        """
        Adds a new line after the specified line.
        """
        self.note.insert(linum + 1, '')
    def remove_line(self, linum: int):
        """
        Removes the line at the specified line.
        """
        self.note.pop(linum)
