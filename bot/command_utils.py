def getCommand(message):
    try:
        return message.content[1 : message.content.index(" ")]
    except ValueError:
        return message.content[1:]


def getCommandArguments(message):
    try:
        return message.content[message.content.index(" ") :]
    except ValueError:
        return None
