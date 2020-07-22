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
        if message.content == "!exit":
            self.close()
            self.destroy()
        if not message.content.startswith(self.delimiter):
            return

        command = getCommand(message)

        if command not in self.commandRegistry:
            return

        arguments = getCommandArguments(message)
        commandObject = self.commandRegistry[command]

        if commandObject.isAsync:
            result = await commandObject.runCommand(arguments)
        else:
            result = commandObject.runCommand(arguments)

        if commandObject.responseType == "text":
            if isinstance(result, list):
                for r in result:
                    await message.channel.send(r)
            else:
                await message.channel.send(result)
        elif commandObject.responseType == "embed":
            if isinstance(result, list):
                for r in result:
                    await message.channel.send(embed=r)
            else:
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
