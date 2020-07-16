import discord

from collections import defaultdict
from collections import namedtuple

from random import choice
from random import randint

from .base_command import BaseSyncCommand
from CP2020_Discord_Bot_API.api.stats import StatBlock
from CP2020_Discord_Bot_API.api.util import CPDataHandler
from CP2020_Discord_Bot_API.api.equipment.weapons import WeaponsHandler


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


def AddWeapons(e, weaponList):
    wtuple = namedtuple("wtuple", ["width", "key"])
    weaponColWidths = defaultdict(lambda: 0)
    for t in [wtuple(width=len(k), key=k) for w in weaponList for k in w] + [
        wtuple(width=max(weaponColWidths[k], len(str(w[k]))), key=k)
        for w in weaponList
        for k in w
    ]:
        weaponColWidths[t.key] = t.width

    weaponColFormat = "{{name:^{name}}}\t{{type:^{type}}}\t{{wa:^{wa}}}\t{{concealability:^{concealability}}}\t{{availability:^{availability}}}\t{{damage}}\({{ammo_type}}\)\t{{shots:^{shots}}}\t{{rate_of_fire:^{rate_of_fire}}}\t{{reliability:^{reliability}}}\t{{range:^{range}}}".format(
        **weaponColWidths
    )

    weaponsTable = "```"
    weaponsTable += "\n".join([weaponColFormat.format(**w) for w in weaponList])
    weaponsTable += "```"

    e.add_field(name="Weapons", value=weaponsTable, inline=False)


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
        self.weaponHandler = WeaponsHandler()

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

        response = discord.Embed(color=0xDD0000)
        AddWeapons(
            response, [self.randomWeapon() for n in range(0, randint(1, 3))]
        )

        responses.append(response)

        return responses

    def randomWeapon(self):
        return self.weaponHandler.getRandomWeapon(
            choice(self.weaponHandler.getWeaponCategories())
        )
