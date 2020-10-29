# bot.py
# Generic Import
import os
from dotenv import load_dotenv

# Discord Imports
from discord.ext import commands

# env loads
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# bot prefix
bot = commands.Bot(command_prefix='!')


# bot events
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


# bot commands
@bot.command(name='rules', help='responds with a link to the rules')
async def rules(ctx):
    Rules = 'http://rules.sahara-server.com/'
    await ctx.send(Rules)


@bot.command(name='price', help='responds with the price of an item')
async def price(ctx, item):

    await ctx.send(item)


# bot errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


# bot run
bot.run(TOKEN)
