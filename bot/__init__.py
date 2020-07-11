import json
import os
from CP2020_Discord_Bot_API.api.skills import SkillRoller


def getSkillRoller(dataPath, masterSkillsFile, careerSkillsFile):
    """Returns a populated SkillRoller.

    Params:
        dataPath str Path to the data directory.
        masterSkillsFile str Name of master skills file.
        careerSkillsFile str Name of career skills file.
    """
    with open(os.path.join(dataPath, masterSkillsFile)) as msf:
        masterSkillData = json.loads(msf.read())
    with open(os.path.join(dataPath, careerSkillsFile)) as csf:
        careerSkillsFile = json.loads(csf.read())

    return SkillRoller(
        masterSkillData,
        careerSkillsFile["career skills"],
        careerSkillsFile["roles"],
    )
