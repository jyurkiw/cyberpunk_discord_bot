from random import choice, randint

COMBAT_TIERS = ([1, 3, 7], [6, 8])
SOCIAL_TIERS = ([3, 4, 5], [0, 8])
BOOSTER_TIERS = ([8, 7], [1, 2])
TECH_TIERS = [0, 2]


class StatBlock(object):
    """A cyberpunk stat block.
    0. int
    1. ref
    2. tech
    3. cool
    4. attr
    5. luck
    6. ma
    7. body
    8. emp
    """

    def __init__(self):
        self.intelligence = 0
        self.reflex = 0
        self.tech = 0
        self.cool = 0
        self.attractivness = 0
        self.luck = 0
        self.movementAllowance = 0
        self.body = 0
        self.empathy = 0

    def __str__(self):
        return "{0} {1} {2} {3} {4} {5} {6} {7} {8}\nTotal: {9}".format(
            self.intelligence,
            self.reflex,
            self.tech,
            self.cool,
            self.attractivness,
            self.luck,
            self.movementAllowance,
            self.body,
            self.empathy,
            self.intelligence
            + self.reflex
            + self.tech
            + self.cool
            + self.attractivness
            + self.luck
            + self.movementAllowance
            + self.body
            + self.empathy,
        )


def setStatBlock(statBlock, stats):
    if len(stats) != 9:
        raise Exception("Statblocks require 9 values.")

    statBlock.intelligence = stats[0]
    statBlock.reflex = stats[1]
    statBlock.tech = stats[2]
    statBlock.cool = stats[3]
    statBlock.attractivness = stats[4]
    statBlock.luck = stats[5]
    statBlock.movementAllowance = stats[6]
    statBlock.body = stats[7]
    statBlock.empathy = stats[8]

    return statBlock


def randomStatBlockFactory():
    """Returns a completely random statblock.
    All stats fall between 1 and 10.
    """
    return setStatBlock(StatBlock(), [randint(1, 10) for i in range(0, 9)])


def orderStats(baseStats, priorityList):
    stats = []
    for idx in priorityList:
        stats.append(baseStats[idx])
    return stats


def genStatsWithMaxTotal(maxStats):
    if maxStats < 40:
        raise Exception("Non-random statblocks must have a max of at least 40")
    maxStats -= 9
    stats = [1] * 9
    statSource = [i for i in range(0, 9)]
    for i in range(0, maxStats):
        idx = choice(statSource)
        stats[idx] += 1
        if stats[idx] == 10:
            statSource.remove(idx)
    return stats


def priorityStatBlockFactory(priorityList):
    """Returns a random statblock ordered based on a passed priority list.
    The priority list is a length 9 List of integers from 0 to 9 with no
    repeated values.
    """
    newStats = [randint(2, 10) for i in range(0, 9)]
    newStats.sort(reverse=True)
    stats = orderStats(newStats, priorityList)

    return setStatBlock(StatBlock(), stats)


def priorityStatBlockWithTotalFactory(priorityList, maxStats):
    """Returns a random, prioritized statblock with a given total.
    """
    newStats = genStatsWithMaxTotal(maxStats)
    newStats.sort(reverse=True)
    stats = orderStats(newStats, priorityList)

    return setStatBlock(StatBlock(), stats)


def priorityListFromTiers(*tiers):
    """Returns a random priority list.
    Tiers are lists of indexes.
    Tier values are consumed at random until every value has been consumed one
    tier at a time.
    Non-tier values are added after all tiers have been consumed.
    """
    flatTiers = [item for sdixList in tiers for item in sdixList]
    priorities = [i for i in range(0, 10)]
    if len(set(flatTiers)) < len(flatTiers):
        raise Exception("Attribute indexes can only occur once")
    priorityList = []
    for tier in tiers:
        while tier:
            p = choice(tier)
            priorityList.append(p)
            tier.remove(p)
            priorities.remove(p)
    while priorities:
        p = choice(priorities)
        priorityList.append(p)
        priorities.remove(p)
    return priorityList


def formatBasicStatblock(statBlock):
    return """
###################################
# INT [ {0:^2} ]  REF [ {1:^2} / {1:^2} ]  TECH [ {2:^2} ]  COOL [ {3:^2} ]
# ATTR [ {4:^2} ]  LUCK [ {5:^2} ]  MA [ {6:^2} ]  BODY [ {7:^2} ]
# EMP [ {8:^2} / {8:^2} ]  RUN [ {9:2} ]  LEAP [ {10:^3.1f} ]  LIFT [ {11:^3} ]
###################################
""".format(
        statBlock.intelligence,
        statBlock.reflex,
        statBlock.tech,
        statBlock.cool,
        statBlock.attractivness,
        statBlock.luck,
        statBlock.movementAllowance,
        statBlock.body,
        statBlock.empathy,
        statBlock.movementAllowance * 3,
        (statBlock.movementAllowance * 3) / 4,
        statBlock.body * 40,
    )
