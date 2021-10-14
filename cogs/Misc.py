from datetime import datetime, timedelta
import discord
from discord import embeds
from discord import colour
from discord import message 
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
    @commands.command()
    async def pool(self,ctx,*choices):
        reactions = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟"
        ]
        if(len(choices) > 10):
            await ctx.send('I dont take more then 10 choices.Ask Your lil Dick :blush:')
            return
        des =""
        for index,choice in enumerate(choices):
            des +=f'{reactions[index]} {choice}\n\n'
        embed = discord.Embed(title = "Pool",colour = ctx.author.color, timestamp = datetime.utcnow(),description = des)
        embed.set_footer(text= f"Pool created by {ctx.author.name}")
        embed.set_thumbnail(url= ctx.author.avatar_url)    
        message = await ctx.send(embed = embed)

        for index in range(len(choices)):
            await message.add_reaction(reactions[index])


def setup(client):
    client.add_cog(Misc(client))