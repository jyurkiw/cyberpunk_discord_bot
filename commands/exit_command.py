from .base_command import BaseSyncCommand

import sys


class ExitCommand(BaseSyncCommand):
    def __init__(self):
        super().__init__("exit")

    def runCommand(self, arguments, message=None):
        sys.exit(0)
