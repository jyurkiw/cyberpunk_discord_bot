import os

from dotenv import load_dotenv
from bot.cyberpunk_bot import CyberpunkBotClient
from bot.table_roller import getTableRoller
from bot import getSkillRoller
from commands.exit_command import ExitCommand
from commands.wastable_commands import GenerateWastableStatsCommand
from commands.wastable_commands import GenerateWastableCommand

from CP2020_Discord_Bot_API.api.util import CPDataHandler
from CP2020_Discord_Bot_API.api.lifepath.siblings import SiblingsModule


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    dataDir = os.getenv("DATA_DIR")

    # Build the table roller
    tableRoller = getTableRoller(dataDir, "tables_config.json")
    tableRoller.familyBackground.registerRollModule("Siblings", SiblingsModule)

    # Build the skill roller
    skillRoller = getSkillRoller(
        dataDir, "master_skill_list.json", "career_skills.json",
    )

    # Build the bot
    bot = CyberpunkBotClient()
    bot.registerCommandObject(ExitCommand())
    bot.registerCommandObject(GenerateWastableStatsCommand())
    bot.registerCommandObject(GenerateWastableCommand(tableRoller, skillRoller))

    bot.run(token)
