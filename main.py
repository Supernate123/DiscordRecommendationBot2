import json
import os
import random
from random import randint

import discord
from discord.ext import commands
from dotenv import load_dotenv
from recommender import search

#pull environment variables from the .env file if they cannot be found in your OS environment
load_dotenv()

#create global variable
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')
# declare global variable

# intents form a list of actions that your bot may want to take on your server
# by default we enable every possible action except three special intents
intents = discord.Intents.default()
# message_content intent lets the bot read other user messages, this is absolutely necessary or else
# the bot cannot tell if people are using commands
intents.message_content = True

# Load the configuration file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Access the prefix from the config
command_prefix = config['prefix']

bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.add_command(search)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name="rps")
async def rps(ctx, playerChoice):
    choice = randint(0, 2)

    if playerChoice == "🪨":
        if (choice == 0):
            await ctx.send("I chose: :rock: It's a tie!")
        if (choice == 1):
            await ctx.send("I chose: :page_facing_up:  I win!")
        if (choice == 2):
            await ctx.send("I chose: :scissors: You win!")
    if playerChoice == "📄":
        if (choice == 0):
            await ctx.send("I chose: :rock: You win!")
        if (choice == 1):
            await ctx.send("I chose: :page_facing_up:  It's a tie!")
        if (choice == 2):
            await ctx.send("I chose: :scissors: I win!!")
    if playerChoice == "✂️":
        if (choice == 0):
            await ctx.send("I chose: :rock: I win!")
        if (choice == 1):
            await ctx.send("I chose: :page_facing_up:  You win!")
        if (choice == 2):
            await ctx.send("I chose: :scissors: It's a tie!")

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("🪨")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("pong!")

@bot.command(name="greet")
async def greeting(ctx, name):
    await ctx.send(f"Hi {name}")

def main():
    bot.run(DISCORD_BOT_TOKEN)

# If this script is run (instead of imported), start the bot.
if __name__ == '__main__':
    main()