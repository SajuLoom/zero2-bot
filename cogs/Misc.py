from datetime import timedelta
import discord
from discord import embeds
from discord import colour 
from discord.ext import commands
from discord.member import Member

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dm(self,ctx,user: discord.Member,*, message = None):
        embed = discord.Embed(title =message, colour = (discord.Colour.magenta()) )
        await user.send(embed = embed)
        await ctx.send("'" + message +"' is sent to "+ user.display_name+", Fucking piece of shit")

def setup(client):
    client.add_cog(Misc(client))