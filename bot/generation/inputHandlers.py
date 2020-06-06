from bot.generation.statBlock import randomStatBlockFactory

# from bot.generation.statBlock import priorityStatBlockFactory
# from bot.generation.statblock import priorityStatBlockWithTotalFactory

from bot.generation.statBlock import formatBasicStatblock


async def generationHandler(cmd, message):
    genType = cmd.pop(0)
    if genType in GENERATION_SUBCOMMANDS:
        result = GENERATION_SUBCOMMANDS[genType](cmd)
        await message.channel.send(result)


def generateStatblock(cmd):
    if not cmd:
        return formatBasicStatblock(randomStatBlockFactory())


GENERATION_SUBCOMMANDS = {
    "statblock": generateStatblock,
    "sb": generateStatblock,
}
