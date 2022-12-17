# testbot.py
import os
import re
import discord
# TODO music
# import youtube_dl
import json
import asyncio
import random
# import numpy as np
from dotenv import load_dotenv
from discord.ext import commands,tasks
from discord.utils import get
from itertools import cycle

load_dotenv()
TOKEN = os.getenv('TOKEN')
# TOKEN = os.environ('TOKEN')
#os.chdir(r'C:\Users\ra\Desktop\pythonstf\dis')
#prefix avah
prefixes_file = "assets/prefixes.json"
def get_prefix(client, message):
    with open(prefixes_file, 'r') as f:
        prefixes = json.load(f)
        f.close()
    return prefixes[str(message.guild.id)]

#namaig shalgah
def is_it_me(ctx):
    return ctx.author.id == 413609867258101760

#utga onooj bn
intents = discord.Intents.all()
intents.members = True
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = get_prefix, intents=intents)
# print (bot.__dict__)

status = cycle(['hithere', 'prefix(--)', '--help'])
texts = ['hithere', 'prefix(--)', '--help']
myguild = 760862411564515368
m = {}
sedvuud = []
availableEmotes = []
rname = "role"
rnumber = 0
with open('assets/emotes.txt','r') as f:
    availableEmotes = f.read().split('\n')

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
    # print(discord.Client.get_guild(myguild).members)
    #for member in guild.members:
        #print(member)
    print(bot.get_guild(myguild).member_count)
    with open("assets/users.json", "r") as j:
        m = json.load(j)
        j.close()
    with open('assets/mysedev.txt','r') as f:
        for i in f:
            a = i[:-1]
            sedvuud.append(a)
    if len(m) == 0:
        m = {}
        for member in guild.members:
            if not member.bot:
                #print(member)
                m[str(member.id)] = {"level" : 1, "xp" : 0, "messageCountdown" : 0, "stage" : 0}
                with open("assets/users.json", "w") as j:
                    json.dump(m, j, indent=4)
                    j.close()
    #await bot.change_presence(activity=discord.Game('prefix(--)'), status=discord.Status.idle)
    await bot.change_presence(activity=discord.Game('nothing'))
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
# @tasks.loop(seconds=5)
# async def change_status():
#     #await bot.change_presence(activity=discord.Game(next(cycle(texts))))
#     await bot.change_presence(activity=discord.Game('depressed game'))


@bot.event
async def on_member_join(member):
    """ channel = discord.utils.get(member.guild.text_channels, name="join-leave")
    await channel.send(f"{member} орж ирлээ!") """
    m[str(member.id)] = {"level": 1, "xp" : 0, "messageCountdown" : 0, "stage" : 0}
    channel = bot.get_channel(760884501969895496) # replace id with the welcome channel's id
    await channel.send(f"{member.mention} орж ирлээ!")
@bot.event
async def on_guild_join(guild):
    with open(prefixes_file, 'r') as f:
        prefixes = json.load(f)
        f.close()
    prefixes[str(guild.id)] = '--'
    with open(prefixes_file, 'w') as f:
        json.dump(prefixes, f, indent = 4)
        f.close()

@bot.event
async def on_guild_remove(guild):
    with open(prefixes_file, 'r') as f:
        prefixes = json.load(f)
        f.close()
    prefixes.pop(str(guild.id))
    with open(prefixes_file, 'w') as f:
        json.dump(prefixes, f, indent = 4)
        f.close()
# @bot.event
# async def on_message_delete(message):
#     msg = str(message.author)+ 'deleted message in '+str(message.channel)+': '+str(message.content)
#     channel = bot.get_channel(781195212222890024)
#     await channel.send(msg)
    #print(msg)

@bot.command()
@commands.has_permissions(administrator = True)
async def changePrefix(ctx, prefix):
    with open(prefixes_file, 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    texts[1] = 'prefix('+prefix+')'
    texts[2] = prefix+'help'
    # status = cycle(['hithere', f'prefix({texts[1]})', f'{texts[2]}help'])
    with open(prefixes_file, 'w') as f:
        json.dump(prefixes, f, indent = 4)
    #client.loop.create_task(bot.change_presence(activity=discord.Game(next(cycle(texts)))))
    await ctx.send(f'Prefix {prefix} болж солигдлоо')

def getEmoji(emoji):
    return str(discord.utils.get(bot.emojis, name=emoji))

# send gifs
@bot.event
async def on_message(message):
    prefix = get_prefix(0, message)
    messageWithoutPrefix = message.content.replace(prefix, '')
    if messageWithoutPrefix in availableEmotes:
        await message.channel.send(getEmoji(messageWithoutPrefix))
    else:
        await bot.process_commands(message)

#commands
@bot.command()
async def pzda(ctx):
    await ctx.send('pzda2')
@bot.command()
async def emotes(ctx):
    helptext = ""
    i = 1
    for command in availableEmotes:
        helptext+=f"{command}\t  "
        i = i + 1
        if i % 3 == 0:
            helptext += "\n"
    #helptext+="\t"
    embed = discord.Embed(
        color=discord.Colour(0x1e385b)
    )
    embed.add_field(name='Emotes',value=helptext)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator = True)
async def addEmote(ctx, emote):
    with open('assets/emotes.txt', 'a') as file:
        file.write(f"\n{emote}")
        availableEmotes.append(emote)
        await ctx.send('Emote added')

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
async def khinami(ctx):
    emoji = discord.utils.get(bot.emojis, name='Madge')
    await ctx.send(str(emoji))
@bot.command()
async def tushig(ctx):
    emoji = discord.utils.get(bot.emojis, name='KhurelSimp')
    await ctx.send(str(emoji))
@bot.command()
async def tenger(ctx):
    emoji = ":regional_indicator_f:"
    await ctx.send(emoji)
@bot.command()
async def davaa(ctx):
    emoji = discord.utils.get(bot.emojis, name='KEKW')
    print(str(emoji))
    await ctx.send(str(emoji))
@bot.command()
async def users(ctx):
    await ctx.send(f"# of members: {ctx.guild.member_count}")

@bot.command()
async def madge(ctx):
    msg = await ctx.channel.send('R u mad?')
    await msg.add_reaction(str(discord.utils.get(bot.emojis, name='Madge')))

# lvl stuff
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
async def levelm(ctx,member:discord.Member):
    # member = ctx.author
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
    
@bot.command()
async def leaderboard(ctx):
    d=[]
    for key, value in m.items():
        d.insert(0,[int(key), int(value['xp']), int(value['level'])])
    d.sort(key = lambda x: x[1], reverse=True)
    embed = discord.Embed(
        color=discord.Colour(0x1e385b),
        title="leaderboard"
    )
    textmen = ""
    textxp = ""
    textlvl =""
    for i in range(5):
        id = d[i][0]
        xp = d[i][1]
        lvl = d[i][2]
        #text = text + f"{i+1}.\n"
        textmen += f"{i+1}. {bot.get_user(id).mention} \n"
        textxp += f"{xp}xp \n"
        textlvl += f"{lvl} \n"
    #embed.add_field(name = '№',value=text, inline=True)
    embed.add_field(name = 'who?',value=textmen, inline=True)
    embed.add_field(name = 'xp',value=textxp, inline=True)
    embed.add_field(name = 'level',value=textlvl, inline=True)
    await ctx.send(embed=embed)

bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx):
    helptext = ""
    i = 1
    for command in bot.commands:
        helptext+=f"{command}\t  "
        i = i + 1
        if i % 3 == 0:
            helptext += "\n"
    #helptext+="\t"
    embed = discord.Embed(
        color=discord.Colour(0x1e385b)
    )
    embed.add_field(name='Командууд',value=helptext)
    await ctx.send(embed=embed)

""" @bot.event
async def on_reaction_add(reaction, user):
  ChID = '761455754900406304'
  if reaction.emoji == str(discord.utils.get(bot.emojis, name='Madge')):
    #CSGO = discord.utils.get(user.server.roles, name="CSGO_P")
    await bot.send_message(ChID, "sda") """
#clear check
""" @bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('комманд олдсонгүй')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('шаардлагатай утгуудыг оруулна уу') """

@bot.command()
@commands.check(is_it_me)
async def addxp(ctx, arg1 : int):
    m[str(ctx.author.id)]['xp'] += arg1
    await ctx.send(f"xp-г чинь одоо {m[str(ctx.author.id)]['xp']} болсон")
@bot.command()
@commands.check(is_it_me)
async def addxpm(ctx, member : discord.Member, arg1 : int):
    id = member.id
    m[str(id)]['xp'] += arg1
    await ctx.send(f"{member.mention}-н xp-г {m[str(id)]['xp']} болгоцон шүү")
    cur_xp = m[str(id)]['xp']
    cur_lvl = m[str(id)]['level']
    levelAhisan = False
    #      (4 * x^3)/5    
    while cur_xp > round((4 * (cur_lvl ** 3 )) / 5):
        cur_lvl += 1
        m[str(id)]['level'] += 1
        levelAhisan = True
    if levelAhisan:
        await ctx.send(f"{member.mention} level ахиж {m[str(id)]['level']} боллоо")
@bot.command()
#@commands.check(is_it_me)
async def subxp(ctx, arg1 : int):
    m[str(ctx.author.id)]['xp'] -= arg1
    if m[str(ctx.author.id)]['xp'] < 0:
        m[str(ctx.author.id)]['xp'] = 0
    await ctx.send(f"xp-гээ чи өөрөө л хасаад {m[str(ctx.author.id)]['xp']} болгосон, би буруугүй шүү")
@bot.command()
@commands.check(is_it_me)
async def subxpm(ctx, member : discord.Member, arg1 : int):
    m[str(member.id)]['xp'] -= arg1
    if m[str(member.id)]['xp'] < 0 :
        m[str(member.id)]['xp'] = 0
    await ctx.send(f"Хэн {member.mention}-ий xp-г хасаад {m[str(member.id)]['xp']} болгочвоо")
    cur_xp = m[str(id)]['xp']
    cur_lvl = m[str(id)]['level']
    levelBuursan = False
    #      (4 * x^3)/5    
    while cur_xp < round((4 * (cur_lvl ** 3 )) / 5):
        cur_lvl -= 1
        m[str(id)]['level'] -= 1
        levelBuursan = True
    if levelBuursan:
        await ctx.send(f"{member.mention} level буурч {m[str(id)]['level']} боллоо")

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
    
# load extension
# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         bot.load_extension(f'cogs.{filename[:-3]}')

# @bot.command(pass_context=True,aliases=['j'])
# async def join(ctx):
#     global voice
#     channel = ctx.message.author.voice.channel
#     voice = get(bot.voice_clients, guild = ctx.guild)
    
#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect()
#         print(f"Bot server luu orloo server - {channel}\n")
        
#     """ await voice.disconnect()
#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect() """
#     await ctx.send(f"{channel} руу орлоо")
    
# @bot.command(pass_context=True,aliases=['l'])
# async def leave(ctx):
#     channel = ctx.message.author.voice.channel
#     voice = get(bot.voice_clients, guild = ctx.guild)
    
#     if voice and voice.is_connected():
#         await voice.disconnect()
#         print(f"Bot {channel}-aas garlaa\n")
#         # await ctx.send(f"{channel}-с гарлаа")
#     else:
#         await ctx.send(f"Намайг хаанаас гаргах гээд байгаан???")
#         print(f"Би ямар нэгэн channel-д байхгүй байна.\n")
        

# @bot.command(pass_context=True,aliases=['p'])
# async def play(ctx, url:str):
    
#     channel = ctx.message.author.voice.channel
#     voiceChannel = get(ctx.guild.voice_channels, name = channel)
#     voice = get(bot.voice_clients, guild = ctx.guild)
    
#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect()
        
#     song_there = os.path.isfile("song.mp3")
#     try:
#         if song_there:
#             os.remove("song.mp3")
#             print("huuchin duug ustgalaa")
#     except PermissionError:
#         print("trying to delete song file, but it's being played")
#         await ctx.send("aldaa: duu togloj baina")
#         return
    
#     await ctx.send("боловсруулж байна")
    
#     voice = get(bot.voice_clients, guild=ctx.guild)
    
#     ydl_opts = {
#         'format' : 'bestaudio/best',
#         'postprocessors':[{
#             'key':'FFmpegExtractAudio',
#             'preferredcodec':'mp3',
#             'preferredquality':'192'
#         }],
#     }
    
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         print("tataj baina")
#         ydl.download([url])
        
#     for file in os.listdir("./"):
#         if file.endswith(".mp3"):
#             name = file
#             print(f"renamed file : {file}\n")
#             os.rename(file,"song.mp3")
    
#     voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: print(f"{name} togluulj duuslaa"))
#     voice.source = discord.PCMVolumeTransformer(voice.source)
#     voice.source.volume = 0.07
    
#     nname = name.rsplit("-", 2)
#     nname.pop()
#     '-'.join(nname)
#     embed = discord.Embed(color = 0x1e385b)
    # embed.add_field(name='Playing:', value = f"[{nname}]({url})")
    
#     await ctx.channel.purge(limit=1)
#     # await ctx.send(f"Playing: {nname}")
#     await ctx.send(embed=embed)
#     print("playing\n")

# @bot.command(pass_context=True)
# async def pause(ctx):
#     voice = get(bot.voice_clients, guild = ctx.guild)
#     if voice.is_playing():
#         voice_pause()
#     else:
#         await ctx.send("Тоглуулж байгаа дуу алга.")    
        
# @bot.command(pass_context=True)
# async def resume(ctx):
#     voice = get(bot.voice_clients, guild = ctx.guild)
#     if voice.is_paused():
#         voice.resume()
#     else:
#         await ctx.send("Дуу зогсоогүй байна")
        
# @bot.command(pass_context=True)
# async def stop(ctx):
#     voice = get(bot.voice_clients, guild = ctx.guild)
#     voice.stop()



#vc shit
# sedev1 = np.array(['Улс төр', 'Эдийн засаг', 'Анимэ', 'Кино урлаг'])
tempBol = False
# @bot.command()
# async def add(ctx, str):
#     for i in sedev1:
#         if sedev1[i] == str:
#             tempBol = True
#             break
#     if tempBol:
#         ctx.send('Байдаг сэдэв байна, бро')
#     np.append(sedev1, str)
#     ctx.send('Сэдэв нэмэгдлээ.')
# @bot.event
# async def testChange(member, before, after):
#     if before.channel:
#         await testRealChange(member, before.channel)
#     if after.channel:
#         await testRealChange(member, after.channel)
# async def testRealChange(member, voice_channel):
#     try:
#         p = re.compile('(.*)\s\((.*?)\)')
#         m = p.search(voice_channel.name)
#         await voice_channel.edit(name = "zda")
#     except Forbidden:
#         print("permission algaa")
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

""" @bot.event
async def on_message(message):
    id = str(message.author.id)
    #if not user.id in users:
    global m
    
    #if message.content == "--stowp" and message.author.id == 413609867258101760:
    # if not id in m:
    #     m[id] = {"xp" : 0, "messageCountdown" : 0}
    #     with open("assets/users.json", "w") as j:
    #         json.dump(m, j)
    #     #await bot.close()
    # if message == "--xp":
    #     await message.channel.send(m[str(message.author.id)]["xp"])
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
                
            with open("assets/users.json", "w") as j:
                json.dump(m, j, indent=4)
                j.close()
    await bot.process_commands(message) """

@bot.command()
@commands.has_permissions(administrator = True)
async def testRole(ctx):
    member = ctx.author
    Role = discord.utils.get(member.guild.roles, name="testRole")
    await member.add_roles(Role)
    await ctx.send(f"{member.mention}, {Role} role-той боллоо")

@bot.command()
@commands.has_permissions(administrator = True)
async def changeCh(ctx, *, new_name):
    await ctx.author.voice.channel.edit(name = new_name)    
@bot.command()
@commands.has_permissions(administrator = True)
async def changeCh1(ctx, channel: discord.VoiceChannel, *, new_name):
    await channel.edit(name = new_name)    
huuchinNer = {}
@bot.command()
@commands.has_permissions(administrator = True)
async def changeback(ctx):
    b = []
    for i,j in huuchinNer.items():
        # channel = bot.get_channel(f"{j[1]}")
        print(j[1])
        myguilda = bot.get_guild(myguild)
        channel = get(myguilda.voice_channels, name = j[0], id = j[1] ) 
        print(channel)
        print(i)
        b.append(i)
        await channel.edit(name = i)
    for i in b:
        del huuchinNer[i]

@bot.command()
async def sedev(ctx):
    randomSedev = sedvuud[random.randint(0, len(sedvuud) - 1)]
    # odoo baigaa ner huuchin nerend baigaag shalgaj baina
    if any(ctx.author.voice.channel.name in k for k in huuchinNer.values()):
        for i, j in huuchinNer:
            if ctx.author.voice.channel.name == j:
                # herev baival solino
                huuchinNer[i] = [randomSedev, ctx.author.voice.channel.id]
    else:
        # baihgui bol shineer uusgene
        huuchinNer[ctx.author.voice.channel.name] = [randomSedev, ctx.author.voice.channel.id]
    
    # print(huuchinNer[ctx.author.id])
    await ctx.send(randomSedev)
    voice_state = ctx.author.voice
    if not voice_state is None:
        randomSedev = randomSedev[0:50]
        print(huuchinNer[ctx.author.voice.channel.name])
        await voice_state.channel.edit(name = f"{randomSedev}")
        print('awaitied i think')
    else:
        print('ur code is trash')
        

        
bot.run(TOKEN)
