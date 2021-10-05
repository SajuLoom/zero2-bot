import discord 
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def spam(self,ctx,member:discord.Member,amount = 5):
        for i in range(amount):
            await ctx.send(f'{member.mention}')

def setup(client):
    client.add_cog(Example(client))