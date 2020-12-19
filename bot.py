import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv("./development.env")

token = os.getenv("DISCORD_BOT_TOKEN")
server = os.getenv("DISCORD_SERVER")
intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!")


@bot.command(name="addrole", help="plans to add you to a game(role)")
async def add_role(context, game):
    await context.send(f"Game identified {game}")


@bot.command(name="random", help="all hell breaks loose")
@commands.has_role('dota')
async def add_role(context):
    await context.send(f"All hell breaks loose")


async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You dont have access to execute this command')


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    guild = client.guilds[0]  # authenticated guild is atlantis
    for members in guild.members:
        print(members)
    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to my Discord server!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "say:" in message.content.lower():
        await message.channel.send(message.content.replace("say:", ""))
    elif "crash-bot" == message.content:
        raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs):
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise


# client.run(token)
bot.run(token)