import discord

from collections import defaultdict
from collections import namedtuple

from random import choice
from random import randint

from io import StringIO

from .base_command import BaseSyncCommand
from CP2020_Discord_Bot_API.api.stats import StatBlock
from CP2020_Discord_Bot_API.api.equipment.weapons import WeaponsRoller
from CP2020_Discord_Bot_API.api.lifepath import LifepathRoller
from CP2020_Discord_Bot_API.api.skills import SkillRoller


class GenerateWastableCommand(BaseSyncCommand):
    def __init__(self, dbName):
        super().__init__("gen-w")
        self.weaponsRoller = WeaponsRoller(dbName)
        self.lifepathRoller = LifepathRoller(dbName)
        self.skillsRoller = SkillRoller(dbName)

    def runCommand(self, arguments, message=None):
        sb = StatBlock().generateRandom().toDict()
        role, sks = self.skillsRoller.rollRandomRole(
            sb["int"] + sb["ref"], points=40
        )
        lp = self.lifepathRoller.rollLifepath()
        wps = [
            self.weaponsRoller.getRandomWeapon()
            for n in range(0, randint(1, 3))
        ]

        output = StringIO()
        self.formatHeader(output, role=role)

        return output.getvalue()

    def formatHeader(self, output, handle=None, role=None):
        if not role:
            raise Exception("Role is required.")

        output.write("Handle: Not Yet Implemented\n")
        output.write("Role: " + role)

    def formatWeapons(self, output, weaponList):
        wtuple = namedtuple("wtuple", ["width", "key"])
        weaponColWidths = defaultdict(lambda: 0)
        for t in [
            wtuple(width=len(k), key=k) for w in weaponList for k in w
        ] + [
            wtuple(width=max(weaponColWidths[k], len(str(w[k]))), key=k)
            for w in weaponList
            for k in w
        ]:
            weaponColWidths[t.key] = t.width

        weaponColFormat = "{{name:^{name}}}\t{{type:^{type}}}\t{{wa:^{wa}}}\t{{concealability:^{concealability}}}\t{{availability:^{availability}}}\t{{damage}}\({{ammo_type}}\)\t{{shots:^{shots}}}\t{{rate_of_fire:^{rate_of_fire}}}\t{{reliability:^{reliability}}}\t{{range:^{range}}}".format(
            **weaponColWidths
        )

        output.write(
            "\n".join([weaponColFormat.format(**w) for w in weaponList])
        )
