import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self,client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot ажиллаж байгаа')

    @commands.command()
    async def pang(self,ctx):
        await ctx.send('aaa')
        
def setup(client):
    client.add_cog(Example(client))