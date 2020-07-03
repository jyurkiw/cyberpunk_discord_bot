import os

from dotenv import load_dotenv
from bot.cyberpunk_bot import CyberpunkBotClient
from commands.exit_command import ExitCommand
from commands.wastable_commands import GenerateWastableStatsCommand

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    # Build the bot
    bot = CyberpunkBotClient()
    bot.registerCommandObject(ExitCommand())
    bot.registerCommandObject(GenerateWastableStatsCommand())

    bot.run(token)
