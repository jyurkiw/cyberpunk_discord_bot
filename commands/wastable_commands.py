import discord

from .base_command import BaseSyncCommand
from CP2020_Discord_Bot_API.api.stats import StatBlock
from CP2020_Discord_Bot_API.api.util import CPDataHandler


class GenerateWastableStatsCommand(BaseSyncCommand):
    def __init__(self):
        super().__init__("gen-w-stats", "embed")

    def runCommand(self, arguments, message=None):
        sb = StatBlock().generateRandom()
        response = discord.Embed(
            title="Wastable Statblock",
            description="Random wastable with {0} stat points.".format(
                sb.getStatTotal()
            ),
            color=0xDD0000,
        )
        # response.add_field(name="Field1", value="This is field 1", inline=False)
        for stat in sb.stats:
            response.add_field(name=stat.name, value=stat.value, inline=True)

        return response


class GenerateWastableCommand(BaseSyncCommand):
    def __init__(self):
        super().__init__("gen-w", "embed")

    def runCommand(self, arguments, message=None):
        pass
