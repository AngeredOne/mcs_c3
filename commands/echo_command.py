# commands/echo_command.py

from core.command import Command

class EchoCommand(Command):
    def __init__(self):
        super().__init__(name="echo", description="Returns the input message.")

    def execute(self, **kwargs):
        return kwargs.get("message", "")
