import discord

from collections import defaultdict
from collections import namedtuple

from random import choice
from random import randint

from io import StringIO

from .base_command import BaseSyncCommand
from CP2020_Discord_Bot_API.api.stats import StatBlock
from CP2020_Discord_Bot_API.api.equipment import WeaponsRoller
from CP2020_Discord_Bot_API.api.equipment import ArmorRoller
from CP2020_Discord_Bot_API.api.lifepath import LifepathRoller
from CP2020_Discord_Bot_API.api.skills import SkillRoller


class ArmorFormatter(object):
    @staticmethod
    def getMaxNameWidth(armorList):
        return max([len(armor["name"]) for armor in armorList])

    @staticmethod
    def getLocationsString(armor):
        return ",".join(
            [l for l in ["head", "torso", "arms", "legs"] if armor[l]]
        )

    @staticmethod
    def getTotalEV(armorList):
        return sum([armor["encumbrance_value"] for armor in armorList])


class GenerateWastableCommand(BaseSyncCommand):
    def __init__(self, dbName):
        super().__init__("gen-w")
        self.weaponsRoller = WeaponsRoller(dbName)
        self.armorRoller = ArmorRoller(dbName)
        self.lifepathRoller = LifepathRoller(dbName)
        self.skillsRoller = SkillRoller(dbName)

    def runCommand(self, arguments, message=None):
        sb = StatBlock().generateRandom()
        sbDict = sb.toDict()
        self.addCalculatedStats(sbDict)

        role, sks = self.skillsRoller.rollRandomRole(
            sbDict["int"] + sbDict["ref"], points=40
        )

        lp = self.lifepathRoller.rollLifepath()

        wps = [
            self.weaponsRoller.getRandomWeapon()
            for n in range(0, randint(1, 3))
        ]
        amr = self.armorRoller.getRandomArmor()

        output = StringIO()
        self.formatHeader(output, role=role, cp=sb.getStatTotal())
        output.write("\n\n")

        self.formatStats(output, sbDict)
        output.write("\n\n")

        self.formatSkills(output, sks)
        output.write("\n\n")

        self.formatWeapons(output, wps)
        output.write("\n\n")

        self.formatArmor(output, amr)
        output.write("\n\n")

        self.formatLifepath(output, lp)

        return output.getvalue()

    def formatHeader(self, output, handle=None, role=None, cp=0):
        """Handle: Not Yet Implemented
        Role: [random role]
        """
        if not role:
            raise Exception("Role is required.")
        if not cp:
            raise Exception("CPs are required.")

        output.write("Handle: Not Yet Implemented\n")
        output.write("Role: " + role + "\tCP: " + str(cp))

    def addCalculatedStats(self, stats):
        stats["run"] = stats["ma"] * 4
        stats["leap"] = stats["run"] / 3
        stats["lift"] = stats["body"] * 40

    def formatStats(self, output, stats):
        output.write(
            "INT [{int}]  REF [{ref}/{ref}]  TECH [{tech}]  COOL [{cool}]\n".format(
                **stats
            )
        )
        output.write(
            "ATTR [{attr}]  LUCK [{luck}]  MA [{ma}]  BODY [{body}]\n".format(
                **stats
            )
        )
        output.write(
            "EMP [{emp}/{emp}]  RUN [{run}]  LEAP [{leap:.1f}]  LIFT [{lift}]".format(
                **stats
            )
        )

    def formatSkills(self, output, skillsList):
        output.write("Skills:\n")
        for skill in skillsList:
            output.write("\t{0} +{1}\n".format(skill.name, skill.score))

    def formatLifepath(self, output, lifepath):
        for stepHeading in lifepath:
            output.write(stepHeading + ":\n")
            for tableResult in lifepath[stepHeading]:
                if "module_key" not in tableResult:
                    output.write("\t")
                    output.write(tableResult["table_name"] + ": ")
                    output.write(tableResult["value"])
                    output.write("\n")

    def formatWeapons(self, output, weaponList):
        """Format and write out passed weapon data.
        """
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

        weaponColFormat = "\t{{name:{name}}}\t{{type:^{type}}}\t{{weapon_accuracy:^{weapon_accuracy}}}\t{{concealability:^{concealability}}}\t{{availability:^{availability}}}\t{{damage}}\({{ammo_type}}\)\t{{shots:^{shots}}}\t{{rate_of_fire:^{rate_of_fire}}}\t{{reliability:^{reliability}}}\t{{range:^{range}}}".format(
            **weaponColWidths
        )

        output.write("Weapons:\n")
        output.write(
            "\n".join([weaponColFormat.format(**w) for w in weaponList])
        )

    def formatArmor(self, output, armorList):
        """Format and write out passed armor data.
        """
        output.write("Armor:\n")
        armorFormatStr = "\t{{name:{nameWidth}}}\t\t{{sp}}\t{{ev}}\t{{locations}}\n".format(
            nameWidth=ArmorFormatter.getMaxNameWidth(armorList)
        )
        stars = ArmorFormatter.getSpStars(armorList)
        for armor in armorList:
            output.write(
                armorFormatStr.format(
                    name=armor["name"],
                    sp=armor["stopping_power"],
                    ev=armor["encumbrance_value"],
                    locations=ArmorFormatter.getLocationsString(armor),
                )
            )
