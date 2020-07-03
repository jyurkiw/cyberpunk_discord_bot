from collections import namedtuple
from CP2020_Discord_Bot_API.api.util import CPDataHandler
import json
import os


def getTableRoller(path, dataFile):
    dataFilePath = os.path.join(path, dataFile)
    if not os.path.exists(dataFilePath):
        raise Exception("{0} not found!".format(dataFilePath))

    with open(dataFilePath, "r") as dataFileList:
        dataFiles = json.loads(dataFileList.read())
        rollerObjects = dict()
        for f in dataFiles:
            if not os.path.exists(os.path.join(path, f["filename"])):
                raise Exception(
                    "{0} datafile does not exist!".format(f["filename"])
                )
            rollerObjects[f["name"]] = CPDataHandler(
                os.path.join(path, f["filename"])
            )
        tableRoller = namedtuple("TableRoller", rollerObjects.keys())(
            **rollerObjects
        )

        return tableRoller
