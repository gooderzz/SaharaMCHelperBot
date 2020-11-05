# bot.py
# Generic Import
import csv
import os
from dotenv import load_dotenv

# Discord Imports
import discord
from discord.ext import commands
from discord.ext import menus

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
    applicationReadyMessage = await me.send(embed=applicationReady)
    await applicationReadyMessage.add_reaction(emoji="\U00002705")
    await applicationReadyMessage.add_reaction(emoji="\U0000274C")

    #Check for Reaction
    await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.emoji == '✅' or reaction.emoji == '❌')
    reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.emoji == '✅' or reaction.emoji == '❌')
    print(reaction)
    if reaction.emoji == '✅' and user == ctx.author:
        await ctx.author.send("Application Next Steps....")
    elif reaction.emoji == '❌' and user == ctx.author:
        await ctx.author.send("Application Cancelled")

@bot.command(name='apply2', help='apply to join the community', pass_context=True)
async def menu_example(ctx):
    m = MyMenu()
    await m.start(ctx)

# bot errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

#Application Ready
applicationReady = discord.Embed(title="Apply For SaharaMC Whitelist", description="Are you ready to apply for SaharaMC's Whitelist? (Use reaction to continue)", color=0x00ff00)
applicationReady.add_field(name=":white_check_mark: Begin", value="Begin filling out the application", inline=True)
applicationReady.add_field(name=":x: Cancel", value="Cancel the application", inline=True)
applicationReady.set_footer(text="You can type cancel at any time to exit")

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

class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        applicant = ctx.author
        return await applicant.send(f'Hello {ctx.author}')

    @menus.button('\N{THUMBS UP SIGN}')
    async def on_thumbs_up(self, payload):
        await self.message.edit(content=f'Thanks {self.ctx.author}!')

    @menus.button('\N{THUMBS DOWN SIGN}')
    async def on_thumbs_down(self, payload):
        await self.message.edit(content=f"That's not nice {self.ctx.author}...")

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()



# bot run
bot.run(TOKEN)

