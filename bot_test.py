import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send("🫵")

client.run("MTQwMjM2MjA3NTQ0NzE2NDk5MQ.GNE-j1.ZQIRmEp2UzyroHfJ7stY39BiTcAWPIofc1YK_w")