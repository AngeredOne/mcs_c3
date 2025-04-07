# commands/add_numbers_command.py

from core.command import Command

class AddNumbersCommand(Command):
    def __init__(self):
        super().__init__(name="add_numbers", description="Adds two numbers.")

    def execute(self, **kwargs):
        return kwargs.get("a", 0) + kwargs.get("b", 0)
