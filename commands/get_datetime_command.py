# commands/get_datetime_command.py

from core.command import Command
from datetime import datetime

class GetDateTimeCommand(Command):
    def __init__(self):
        super().__init__(name="get_datetime", description="Returns the current date and time.")

    def execute(self, **kwargs):
        return datetime.now().isoformat()
