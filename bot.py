# testbot.py
import os
import re
import discord
import json
import asyncio
import numpy as np
from dotenv import load_dotenv
from discord.ext import commands,tasks
from discord.utils import get
from itertools import cycle

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#os.chdir(r'C:\Users\ra\Desktop\pythonstf\dis')
#prefix avah
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

#namaig shalgah
def is_it_me(ctx):
    return ctx.author.id == 413609867258101760

#utga onooj bn
intents = discord.Intents.default()
intents.members = True
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = get_prefix, intents=intents)

status = cycle(['hithere', 'prefix(--)', '--help'])
texts = ['hithere', 'prefix(--)', '--help']
myguild = 760862411564515368
m = {}
rname = "role"
rnumber = 0
@bot.event
async def on_ready():
    print('Logged on.')
    global m
    for guild in bot.guilds:
        if guild.name == myguild:
            break
    """ print(
        f'{bot.user} is connected to the following guild: \n' 
        f'{guild.name} (id: {guild.id})'
    ) """
    #print(discord.Client.get_guild(myguild).members)
    #for member in guild.members:
        #print(member)
    print(bot.get_guild(myguild).member_count)
    with open("users.json", "r") as j:
        m = json.load(j)
        j.close()
    if len(m) == 0:
        m = {}
        for member in guild.members:
            if not member.bot:
                #print(member)
                m[str(member.id)] = {"level" : 1, "xp" : 0, "messageCountdown" : 0, "stage" : 0}
                with open("users.json", "w") as j:
                    json.dump(m, j, indent=4) 
    #await bot.change_presence(activity=discord.Game('prefix(--)'), status=discord.Status.idle)
    #await change_presence(game=discord.Game(name="hithere", type=1))
    while True:
        try:
            for member in guild.members:
                if not member.bot:
                    if m[str(member.id)]["messageCountdown"] >= -1:
                        m[str(member.id)]["messageCountdown"] -= 1
        except:
            pass
        await asyncio.sleep(1)


#activity status
@tasks.loop(seconds=5)
async def change_status():
    #await bot.change_presence(activity=discord.Game(next(cycle(texts))))
    await bot.change_presence(activity=discord.Game('depressed game'))


@bot.event
async def on_member_join(member):
    """ channel = discord.utils.get(member.guild.text_channels, name="join-leave")
    await channel.send(f"{member} орж ирлээ!") """
    m[str(member.id)] = {"level": 1, "xp" : 0, "messageCountdown" : 0, "stage" : 0}
    channel = bot.get_channel(760884501969895496) # replace id with the welcome channel's id
    await channel.send(f"{member.mention} has arrived!")
@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '--'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@bot.command()
@commands.has_permissions(administrator = True)
async def changePrefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    texts[1] = 'prefix('+prefix+')'
    texts[2] = prefix+'help'
    status = cycle(['hithere', f'prefix({texts[1]})', f'{texts[2]}help'])
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
    #client.loop.create_task(bot.change_presence(activity=discord.Game(next(cycle(texts)))))
    await ctx.send(f'Prefix {prefix} болж солигдлоо')

#commands
@bot.command()
async def pzda(ctx):
    await ctx.send('pzda2')
@bot.command()
async def ping(ctx):
    await ctx.send(f'pong {round(bot.latency * 1000)}ms')
@bot.command()
async def zailpzda(ctx):
    await ctx.send('chi uuruu zail')
@bot.command()
async def hengaybe(ctx):
    await ctx.send('nomon')
@bot.command()
async def nomon(ctx):
    emoji = discord.utils.get(bot.emojis, name='BRUH')
    await ctx.send(str(emoji))
@bot.command()
async def huslen(ctx):
    emoji = discord.utils.get(bot.emojis, name='PogO')
    await ctx.send(str(emoji))
@bot.command()
async def duk(ctx):
    emoji = discord.utils.get(bot.emojis, name='Sadjaa')
    await ctx.send(str(emoji))
@bot.command()
async def tushig(ctx):
    emoji = discord.utils.get(bot.emojis, name='KhurelSimp')
    await ctx.send(str(emoji))
@bot.command()
async def users(ctx):
    await ctx.send(f"# of members: {ctx.guild.member_count}")

@bot.command()
async def madge(ctx):
    msg = await ctx.channel.send('R u mad?')
    await msg.add_reaction(str(discord.utils.get(bot.emojis, name='Madge')))

@bot.command()
async def getcd(ctx):
    await ctx.send(f"{m[str(ctx.author.id)]['messageCountdown']} секунд дутуу байна")
    
@bot.command()
async def xp(ctx):
    await ctx.send(f"Танд {m[str(ctx.author.id)]['xp']}xp байна.")

@bot.command()
async def level(ctx):
    member = ctx.author
    member_id = str(member.id)
    embed = discord.Embed(color = member.color)
    """ , timestamp = ctx.message.created_at """
    embed.set_author(name=f"level - {member}", icon_url=member.avatar_url)
            
    #embed.add_field(name='Level', value=self.users[member_id]['level'])
    embed.add_field(name='XP', value=m[member_id]['xp'])
    embed.add_field(name='Level', value=m[member_id]['level'])
    await ctx.send(embed=embed)

@bot.command()
async def getxp(ctx, member : discord.Member):
    await ctx.send(f"{member.mention}-д {m[str(member.id)]['xp']}xp байна.")
    
bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx):
    helptext = ""
    for command in bot.commands:
        helptext+=f"{command}\n"
    #helptext+="\t"
    embed = discord.Embed(
        color=discord.Colour(0x1e385b)
    )
    embed.add_field(name='Командууд',value=helptext)
    await ctx.send(embed=embed)
""" async def help(ctx):
    helptext = "```"
    for command in bot.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext) """    

""" @bot.event
async def on_reaction_add(reaction, user):
  ChID = '761455754900406304'
  if reaction.emoji == str(discord.utils.get(bot.emojis, name='Madge')):
    #CSGO = discord.utils.get(user.server.roles, name="CSGO_P")
    await bot.send_message(ChID, "sda") """
#clear check
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('комманд олдсонгүй')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('шаардлагатай утгуудыг оруулна уу')

@bot.command()
@commands.check(is_it_me)
async def addxp(ctx, arg1 : int):
    m[str(ctx.author.id)]['xp'] += arg1
    await ctx.send(f"xp-г чинь нэмээд {m[str(ctx.author.id)]['xp']} болгоцон шүү")
@bot.command()
#@commands.check(is_it_me)
async def subxp(ctx, arg1 : int):
    m[str(ctx.author.id)]['xp'] -= arg1
    await ctx.send(f"xp-гээ чи өөрөө л хасаад {m[str(ctx.author.id)]['xp']} болгосон, би буруугүй шүү")

@bot.command()
@commands.check(is_it_me)
async def clear(ctx, arg1 : int):
    await ctx.channel.purge(limit=arg1)
    
@bot.command()
@commands.check(is_it_me)
async def whoami(ctx):
    #await ctx.send(f"it's me {ctx.author}")
    await ctx.send('coward')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('asd')

@bot.command()
@commands.check(is_it_me)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
@commands.check(is_it_me)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    
@bot.command()
@commands.check(is_it_me)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#vc shit
sedev1 = np.array(['Улс төр', 'Эдийн засаг', 'Анимэ', 'Кино урлаг'])
tempBol = False
""" @bot.command()
async def add(ctx, str):
    for i in sedev1:
        if sedev1[i] == str:
            tempBol = True
            break
    if tempBol:
        ctx.send('Байдаг сэдэв байна, бро')
    np.append(sedev1, str)
    ctx.send('Сэдэв нэмэгдлээ.')
@bot.event
async def testChange(member, before, after):
    if before.channel:
        await testRealChange(member, before.channel)
    if after.channel:
        await testRealChange(member, after.channel)
async def testRealChange(member, voice_channel):
    try:
        p = re.compile('(.*)\s\((.*?)\)')
        m = p.search(voice_channel.name)
        await voice_channel.edit(name = "zda")
    except Forbidden:
        print("permission algaa") """
""" async def testChange(ctx, channel: discord.VoiceChannel):
    await channel.edit(name='zda') """

def lvl_up(id):
    cur_xp = m[str(id)]['xp']
    cur_lvl = m[str(id)]['level']
        
    if cur_xp > round((4 * (cur_lvl ** 3 )) / 5):
        m[str(id)]['level'] += 1
        return True
    else: 
        return False

@bot.event
async def on_message(message):
    id = str(message.author.id)
    #if not user.id in users:
    global m
    
    #if message.content == "--stowp" and message.author.id == 413609867258101760:
    """ if not id in m:
        m[id] = {"xp" : 0, "messageCountdown" : 0}
        with open("users.json", "w") as j:
            json.dump(m, j) """
        #await bot.close()
    """ if message == "--xp":
        await message.channel.send(m[str(message.author.id)]["xp"]) """
    #elif message.author == bot.user:
    if not message.author.bot:
        if m[id]["messageCountdown"] <= 0:
            m[id]["xp"] += 1
            m[id]["messageCountdown"] = 10
            if lvl_up(message.author.id):
                await message.channel.send(f"{message.author.mention} level ахиж {m[id]['level']} боллоо")
                if m[id]["stage"] * 5 < m[id]["level"]:
                    m[id]["stage"] += 1
                    Role = discord.utils.get(message.guild.roles, name=rname + str(m[id]["stage"]))
                    await message.author.add_roles(Role)
                    await message.channel.send(f"{message.author.mention}, {Role}-г авлаа")
                
            with open("users.json", "w") as j:
                json.dump(m, j, indent=4)
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator = True)
async def testRole(ctx):
    member = ctx.message
    Role = discord.utils.get(member.guild.roles, name="role1")
    await member.author.add_roles(Role)
    await ctx.send(f"{member.author.mention}, {Role} role-той боллоо")


bot.run(TOKEN)
"""client.run("NzYwODg1MDY1NDQ1MTQ2NjI0.X3SjcA.kMfl8iqJByXvHXHHusoCjEC8Y7Y") """
