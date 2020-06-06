import os
import sys
import discord
from dotenv import load_dotenv
from bot.generation.inputHandlers import generationHandler


client = discord.Client()


async def exit(cmd, message):
    sys.exit(0)


COMMANDS = {"gen": generationHandler, "quit": exit}


@client.event
async def on_message(message):
    print(message.content, flush=True)
    if message.content[0] == "!":
        cmd = message.content[1:].split(" ")
        if cmd[0] in COMMANDS:
            await COMMANDS[cmd[0]](cmd[1:], message)


def run():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    client.run(TOKEN)
