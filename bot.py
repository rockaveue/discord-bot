# testbot.py
import os
import re
import discord
import numpy as np
from dotenv import load_dotenv
from discord.ext import commands,tasks
from itertools import cycle

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='--')
status = cycle(['hithere', 'prefix(--)', '--help'])
@bot.event
async def on_ready():
    change_status.start()
    #await bot.change_presence(activity=discord.Game('prefix(--)'), status=discord.Status.idle)
    #await change_presence(game=discord.Game(name="hithere", type=1))
    print('Logged on.')
#activity status
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))
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


#clear check
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('комманд олдсонгүй')
    #if isinstance(error, commands.MissingRequiredArgument):
        #await ctx.send('шаардлагатай утгуудыг оруулна уу')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, arg1 : int):
    await ctx.channel.purge(limit=arg1)
    
def is_it_me(ctx):
    return ctx.author.id == 413609867258101760

@bot.command()
@commands.check(is_it_me)
async def whoami(ctx):
    #await ctx.send(f"it's me {ctx.author}")
    await ctx.send('admin')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('asd')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    
@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


#vc shit
sedev1 = np.array(['Улс төр', 'Эдийн засаг', 'Анимэ', 'Кино урлаг'])
tempBol = False
@bot.command()
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
        print("permission algaa")
""" async def testChange(ctx, channel: discord.VoiceChannel):
    await channel.edit(name='zda') """


#hereggui
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
        
        if message.content == 'gay':
            await message.channel.send('nomon')
client = MyClient()
# client.run(TOKEN)
bot.run(TOKEN)
"""client.run("NzYwODg1MDY1NDQ1MTQ2NjI0.X3SjcA.kMfl8iqJByXvHXHHusoCjEC8Y7Y") """
