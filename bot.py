import os

from dotenv import load_dotenv
from bot.cyberpunk_bot import CyberpunkBotClient
from bot.table_roller import getTableRoller
from bot import getSkillRoller
from commands.exit_command import ExitCommand
from commands.wastable_commands import GenerateWastableCommand

from CP2020_Discord_Bot_API.api.util import CPDataHandler
from CP2020_Discord_Bot_API.api.lifepath.siblings import SiblingsModule

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    dataDir = os.getenv("DATA_DIR")
    dbName = os.getenv("DB_NAME")

    # Build the bot
    bot = CyberpunkBotClient()
    # bot.registerCommandObject(ExitCommand())
    bot.registerCommandObject(GenerateWastableCommand(dbName))

    bot.run(token)
