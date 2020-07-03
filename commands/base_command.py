"""Base command classes for all bot commands.
Commands must register an instance of the command class with the bot before
the bot is run.
The runCommand method is expected to return either *formatted* string data to
the client for display on the discord server, or whatever should be expected
according to the responseType.
"""


class BaseCommand(object):
    def __init__(self, name, isAsync, responseType="text"):
        self.name = name
        self.isAsync = isAsync
        self.responseType = responseType


class BaseSyncCommand(BaseCommand):
    def __init__(self, name, responseType="text"):
        super().__init__(name, False, responseType)

    def runCommand(self, arguments, message=None):
        return "The {0} command is not yet implemented.".format(self.name)


class BaseAsyncCommand(BaseCommand):
    def __init__(self, name, responseType="text"):
        super().__init__(name, True, responseType)

    async def runCommand(self, arguments, message=None):
        yield "The {0} command is not yet implemented.".format(self.name)
