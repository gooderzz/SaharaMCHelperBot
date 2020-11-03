# bot.py
# Generic Import
import csv
import os
from dotenv import load_dotenv

# Discord Imports
import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = discord.Client()

# env loads
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# bot prefix
bot = commands.Bot(intents=intents, command_prefix='!', case_insensitive=True)


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
async def price(ctx, *, item):
    print(item)
    with open('sd_prices.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        print('Shopping Prices Opened')
        item = (item.capitalize())
        print(item)
        for row in csv_reader:
            if row[0].capitalize() == item:
                print(f'{row[0]} costs {row[1]} {row[2]} per {int(row[3])/64} stacks.')
                cost = (f'{row[0]} costs {row[1]} {row[2]} per {int(row[3])/64} stacks.')

    await ctx.send(cost)

@bot.command(name='apply', help='apply to join the community', pass_context=True)
async def apply(ctx):
    me = ctx.author
    print(me, 'is applying')
    application_message = 'Hello!'
    await me.send(embed=embedVar)

# bot errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


#Application Creation
embedVar = discord.Embed(title="Apply For SaharaMC Whitelist", description="This is the application for SaharaMC whitelist", color=0x00ff00)
embedVar.add_field(name="What is your Discord Name?", value="Discord Name", inline=True)
embedVar.add_field(name="What is your minecraft in game name?", value="Minecraft Name", inline=True)
embedVar.add_field(name="What is your age?", value="Age", inline=True)
embedVar.add_field(name="How many hours a day do you play Minecraft?", value="Hours", inline=True)
embedVar.add_field(name="What does a community mean to you?", value="Community", inline=True)
embedVar.add_field(name="What is your favourite part of Minecraft and what do you look forward to doing the most if accepted?", value="Favourite part of Minecraft", inline=True)
embedVar.add_field(name="Please explain a little bit about yourself. Maybe you have something unique that you would like to share. (3-4 sentences minimum please)", value="A little about yourself", inline=True)
embedVar.add_field(name="What will you bring to the community? if you have any great builds you can post a link here. (3-4 sentences minimum please)", value="What will you bring", inline=True)
embedVar.add_field(name="How did you hear about us? If from a website, please enter the website name.", value="Hear about us", inline=True)
embedVar.add_field(name="You do understand SaharaMC is built on trust and that is why we emphasize the importance of the rules. Have you completely read all of the rules? Enter yes or no?", value="Acceptance", inline=True)
embedVar.add_field(name="What is SaharaMC's golden rule?", value="Golden Rule", inline=True)

# bot run
bot.run(TOKEN)

