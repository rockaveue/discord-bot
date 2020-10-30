import discord
from discord.ext import commands

class TextCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    #commands


def setup(client):
    client.add_cog(TextCommands(client))