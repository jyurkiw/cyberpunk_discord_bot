import discord
from .command_utils import getCommand, getCommandArguments


class CyberpunkBotClient(discord.Client):
    def __init__(self, delimiter="!"):
        super().__init__()
        self.delimiter = delimiter
        self.commandRegistry = dict()

    async def on_message(self, message):
        """Overloaded on_message event. Executes registered commands.
        """
        print(message.content, flush=True)
        if not message.content.startswith(self.delimiter):
            print("Message did not start with delimiter", flush=True)
            return

        print("getting command...", flush=True)
        command = getCommand(message)
        print("command: " + command, flush=True)

        if command not in self.commandRegistry:
            print("command not found", flush=True)
            return

        arguments = getCommandArguments(message)

        if arguments:
            print("args: " + arguments, flush=True)

        commandObject = self.commandRegistry[command]

        if commandObject.isAsync:
            result = await commandObject.runCommand(arguments)
        else:
            result = commandObject.runCommand(arguments)

        if commandObject.responseType == "text":
            await message.channel.send(result)
        elif commandObject.responseType == "embed":
            await message.channel.send(embed=result)

    def registerCommandObject(self, commandObject):
        """Register a command object with this bot.
        Command objects must have name and isAsync attributes, and a runCommand
        method implemented.
        RunCommand should execute quickly and must be synchronious.
        isAsync is simply an attribute set to True or False.
        """
        if not hasattr(commandObject, "name"):
            raise Exception("Command objects must have a name attribute.")
        if not hasattr(commandObject, "isAsync"):
            raise Exception("Command objects must have an isAsync attribute.")
        if not hasattr(commandObject, "runCommand"):
            raise Exception(
                "Command objects must implement a runCommand function."
            )
        self.commandRegistry[commandObject.name] = commandObject
