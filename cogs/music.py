from discord.ext import commands
import wavelink
import discord
import datetime
import asyncio
import re
import time
import collections
import discord.utils

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}

# import lavalink

# class MusicCog(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.bot.music = lavalink.Client(self.bot.user.id)
#         self.bot.music.add_node('localhost', 7000, 'hithere', 'sea', 'music-node')
#         self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
#         self.bot.music.add_event_hook(self.track_hook)
        
#     @commands.command(name='join')    
#     async def join(self, ctx):
#         print('join command worked')
        
    
    
#     async def track_hook(self, event):
#         if isinstance(event, lavalink.events.QueueEndEvent):
#             guild_id = int(event.player.guild_id)
#             await self.connect_to(guild_id, None)

#     async def connect_to(self, guild_id: int, channel_id: str):
#         """ Connects to the given voicechannel ID. A channel_id of 'None' means disconnect. """
#         ws = self.bot._connection._get_websocket(guild_id)
#         await ws.voice_state(str(guild_id), channel_id)

class NoVoiceChannel(discord.DiscordException):
    def __init__(self):
        super().__init__('Орох voice channel алга')

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot = self.bot)
        self.bot.loop.create_task(self.start_nodes())
        
        self.queue = collections.deque()
        self.repeat = collections.defaultdict()
        self.queue_index = collections.defaultdict(int)
        self.queue_index = 0
        
    async def start_nodes(self):
        await self.bot.wait_until_ready()
        
        await self.bot.wavelink.initiate_node(
            host = 'https://git.heroku.com/dis-lavalink.git',#127.0.0.1
            port = '80',#7000
            rest_uri = 'https://git.heroku.com/dis-lavalink.git:80',
            password = 'hithere',
            identifier = 'TEST',
            region = 'hong_kong'
        )
        
    async def search(self, ctx, query):
        tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")
        
        if re.match(URL_REGEX, query) is not None:
            for track in tracks:
                if query == track.url:
                    return track
        else:
            def _check(reaction, user):
                return {
                    reaction.emoji in ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣") 
                    #test
                    and user == ctx.author
                    and reaction.message.id == msg.id           
                }
            embed = discord.Embed(
                title = "Дуугаа сонгоно уу"
            )
            fields = [("Үр дүн", "\n".join(f"**{i+1}.** {track.title}" for i, track in enumerate(tracks[:5])), False)]
            
            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline = inline)
                
            msg = await ctx.send(embed = embed)
            
            for emoji in ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣"):
                await msg.add_reaction(emoji)
                
            await ctx.send("bout to sleep")
            time.sleep(0.2)
            await ctx.send("woke up")
            
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = _check, timeout = 30.0)
            except asyncio.TimeoutError:
                pass
            else:
                return tracks[OPTIONS[reaction.emoji]]
    
    def is_connected(self, ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()
    
    async def repeat_one(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.play(self.queue[self.queue_index])
    
    async def repeat_all(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        # if queue := self.queue:
            # queue.rotate(-1)
        self.queue_index = -1
        await player.play(self.queue[0])
    
    async def repeat_none(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.play(self.queue[0])
    
    @wavelink.WavelinkMixin.listener()
    async def on_track_end(self, node, payload):
        if len(self.queue) > self.queue_index + 1:
            self.queue_index += 1
            await payload.player.play(self.queue[self.queue_index])
        # await self.repeat[payload.player.guild_id]()(node, payload)
        # print(f'TRACKEND: {self.queue}')
    
    @commands.command(name = "connect", aliases = ['join', 'j'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        # if channel is None:
        try:
            channel = channel or ctx.author.voice.channel
        except AttributeError:
            # raise discord.DiscordException
            raise NoVoiceChannel()
            
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f"{channel.name}-руу орж байна.")
        await player.connect(channel.id)
        
        
    @commands.command(name = "play", aliases = ['p'])
    async def play_command(self, ctx, *, query: str):
        
        # if not (track := await self.search(ctx, query)):
        #     return await ctx.send("Хайлтын илэрц олдсонгүй")
        
        
        # tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        # if not tracks:
        #     return await ctx.send('Дуу олсонгүй')

        # player = self.bot.wavelink.get_player(ctx.guild.id)
        # if not player.is_connected:
        #     await ctx.invoke(self.connect_)
        #-----------------------------------------
        # hugatsaa = int(track.duration) / 1000
        # hugatsaa = str(datetime.timedelta(seconds=hugatsaa))

        # stitle = (f"Playing: [{track.title}]({query})")
        # embed = discord.Embed(title = stitle)
        # fields = [
        #     ("Оруулсан", track.author, False),
        #     ("Хугацаа", hugatsaa, False),
        # ]

        # for name, value, inline in fields:
        #     embed.add_field(name=name, value=value, inline=inline)
        # await ctx.send(f'{str(tracks[0])} дууг жагсаалтад нэмлээ.')
        
        # if not (player := self.bot.wavelink.get_player(ctx.guild.id)).is_connected:
        #     await ctx.invoke(self.connect_)
        
        # await ctx.send(embed=embed)
        # await player.play(track)
        #-----------------------------------------
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Дуу олсонгүй')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected and not self.is_connected(ctx):
            await ctx.invoke(self.connect_)

        
        
        if not self.queue and not player.is_playing:
            embed_title = "Playing: "
            await player.play(tracks[0])
        else:
            embed_title = "Queued: "
        
        hugatsaa = int(tracks[0].duration) / 1000
        hugatsaa = str(datetime.timedelta(seconds=hugatsaa))

        stitle = (f"{tracks[0].title}")
        embed = discord.Embed(title = embed_title, description = stitle)
        fields = [
            ("Оруулсан", tracks[0].author, False),
            ("Хугацаа", hugatsaa, False),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        # await ctx.send(f'{str(tracks[0])} дууг жагсаалтад нэмлээ.')
        
        await ctx.send(embed=embed)
        self.queue.append(tracks[0])
        print(self.queue)
        print(self.queue_index)
        
        if ctx.author.id == 327066853853757451:
            ctx.send(f'{ctx.author.mention}stupid fuck')
            

    @commands.command(name = 'pause', aliases = ['stfu'])
    async def pause_command(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.set_pause(not player.is_paused)
        await ctx.send("Дууг түр зогсоолоо" if player.is_paused else "Тоглуулж байна.")
    
    @commands.command(name = 'stop')
    async def stop_command(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.set_pause(not player.is_paused)
        await ctx.send('Дууг зогсоолоо')
    
    @commands.command(name = 'resume', aliases = ['g'])
    async def resume_command(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_paused or not player.is_connected:
           return
        await player.set_pause(False)
        
    
    @commands.command(name = 'next', aliases = ['skip'])
    async def skip_command(self,ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        # await player.play(self.queue.popleft())
        
        if len(self.queue) > self.queue_index + 1:
            self.queue_index += 1
            await player.play(self.queue[self.queue_index])
        else:
            await ctx.send("Дараагийн дуу байхгүй байна.")
    
    @commands.command(name = 'queue', aliases = ['q'])
    async def queue_command(self, ctx):
        pass
    
    @commands.command(name = 'disconnect', aliases = ['dc'])
    async def disconnect_command(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send('c u next time')
        await player.disconnect()
        
    @commands.command(name = "repeat")
    async def repeat_command(self, ctx, *, type: str):
        # off, 1, all
        if type == "off":
            self.repeat[ctx.guild.id] = self.repeat_none
            await self.repeat_none(ctx)
        elif type == "1":
            self.repeat[ctx.guild.id] = self.repeat_one
            await self.repeat_one(ctx)
        elif type == "all":
            self.repeat[ctx.guild.id] = self.repeat_all
            await self.repeat_all(ctx)
        
        
        
        
        

def setup(bot):
    # bot.add_cog(MusicCog(bot))
    bot.add_cog(Music(bot))
