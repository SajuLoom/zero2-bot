import discord
from discord.ext.commands.core import command 
import youtube_dl
import pafy
from discord.ext import commands
import asyncio

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.song_queue = {}

        self.setup1()

    def setup1(self):
        for guild in self.client.guilds:
            self.song_queue[guild.id] =[]

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url = False):
        info = await self.client.loop.run_in_executor(None, lambda:youtube_dl.YoutubeDL({"format": "bestaudio","quiet": True}).extract_info(f"ytsearch{amount}:{song}",download = False, ie_key = "YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.client.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("Oops! :face_in_clouds: You are not connected to a voice channel, You can't use this command rigth now")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("Oops! :face_in_clouds: You are not connected to a voice channel, You can't use this command rigth now")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        
        await ctx.send("I disconnected form the voice channel")
    
    @commands.command()
    async def play(self, ctx, *, song =None):
        if song is None:
            return await ctx.send("I can't find any song name.Please mention one")
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song...:hourglass:")

            result = await self.search_song(1, song,get_url= True)

            if result is None:
                return await ctx.send("OOOOps,Can't find the song")
                
            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"Song {song} is Queued")

            else:
                return await ctx.send("Sorry,Queue is full")
        
        await self.play_song(ctx,song)
        await ctx.send(f'Now Playing:\n {song}')
    
    @commands.command()
    async def search(self,ctx,song = None):
        if song is None:
            return await ctx.send("Add a song u Dumb Ass")
        
        await ctx.send("Searching......")

        info = await self.search_song(5,song)

        embed = discord.Embed(
            title = f'Results for {song}:',
            description = "Hope You found what you are looking for\n"
        )

        amount =0
        for entry in info["entries"]:
            embed.description+= f"[{entry['title']}]({entry['webpage_url']})\n"
            amount +=1
        
        await ctx.send(embed = embed)

    @commands.command()
    async def queue(self,ctx):
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue.")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.magenta())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1
        await ctx.send(embed=embed)
    
    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song.")

        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I am not currently playing any songs for you.")

        skip = True

        await ctx.send("You ArsheHoles have Admin Roles.Why do we need vote. Song Skipped")

        if skip:
            ctx.voice_client.stop()

def setup(client):
    client.add_cog(Music(client))