import discord

from .base_command import BaseSyncCommand
from CP2020_Discord_Bot_API.api.stats import StatBlock
from CP2020_Discord_Bot_API.api.util import CPDataHandler


def AddLineBreak(e):
    e.add_field(name="\u200B", value="\u200B", inline=False)


def AddWastableStats(e, sb):
    for stat in sb.stats:
        e.add_field(name=stat.name, value=stat.value, inline=True)


def AddTableResults(e, results):
    for result in results:
        e.add_field(name=result.name, value=result.value, inline=True)


def AddSkills(e, roleName, skills):
    valueFormat = (
        "{0:>" + str(max([len(skill.value) for skill in skills])) + "} +{1}"
    )
    skillTable = "```"
    skillTable += "\n".join(
        [valueFormat.format(skill.value, skill.count) for skill in skills]
    )
    skillTable += "```"

    e.add_field(
        name="Role: {0}".format(roleName), value=skillTable, inline=False
    )

    # for skill in skills:
    #     e.add_field(name=skill.value, value=skill.count, inline=False)


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

        AddWastableStats(response, sb)

        return response


class GenerateWastableCommand(BaseSyncCommand):
    def __init__(self, tableRoller, skillRoller):
        super().__init__("gen-w", "embed")
        self.tableRoller = tableRoller
        self.skillRoller = skillRoller

    def runCommand(self, arguments, message=None):
        sb = StatBlock().generateRandom()
        stats = sb.toDict()
        responses = list()
        response = discord.Embed(
            title="Random Wastable",
            description="Random Wastable with {0} stat points.".format(
                sb.getStatTotal()
            ),
            color=0xDD0000,
        )

        AddTableResults(response, self.tableRoller.motivations.runProcess())
        AddLineBreak(response)
        AddWastableStats(response, sb)
        AddLineBreak(response)
        AddTableResults(
            response, self.tableRoller.originsAndPersonalStyle.runProcess()
        )
        responses.append(response)
        response = discord.Embed(color=0xDD0000)

        role = self.skillRoller.getRandomRole()
        AddSkills(
            response,
            role,
            self.skillRoller.roll(role, stats["int"] + stats["ref"]),
        )
        responses.append(response)

        return responses
