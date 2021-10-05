import asyncio
from datetime import timedelta
import discord
from discord import embeds
from discord.ext import commands
import urllib.parse
from googlesearch import search
from PyDictionary import PyDictionary
class Google(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wiki(self,ctx,*lookfor):
        looking = " ".join(lookfor)
        query = "en.wikipedia.org"+ looking
        buttons= [u'\u23EA', u"\u25C0",u'\u25B6',u'\u23E9']
        current = 0
        results = search(query)
        print(results)
        msg = await ctx.send(results[current])

        for button in buttons:
            await msg.add_reaction(button)
        while True: 
            try:
                reaction, user = await self.client.wait_for("reaction_add",check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout= 60.0)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
            else:
                previous_page = current

                if reaction.emoji == u'\u23EA':
                    current =0
                elif reaction.emoji == u"\u25C0":
                    if(current >0):
                        current -=1
                elif reaction.emoji == u'\u25B6':
                    if current < len(results)-1:
                        current +=1
                elif reaction.emoji == u'\u23E9':
                    current = len(results)-1
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(content =results[current])
            
    @commands.command()
    async def gsearch(self,ctx,*,searchquery: str):
        results = search('<https://www.google.com/search?q={}>'.format(urllib.parse.quote_plus(searchquery)))
        buttons= [u'\u23EA', u"\u25C0",u'\u25B6',u'\u23E9']
        current = 0
        print(results)
        msg = await ctx.send(results[current])

        for button in buttons:
            await msg.add_reaction(button)
        while True: 
            try:
                reaction, user = await self.client.wait_for("reaction_add",check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout= 60.0)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
            else:
                previous_page = current

                if reaction.emoji == u'\u23EA':
                    current =0
                elif reaction.emoji == u"\u25C0":
                    if(current >0):
                        current -=1
                elif reaction.emoji == u'\u25B6':
                    if current < len(results)-1:
                        current +=1
                elif reaction.emoji == u'\u23E9':
                    current = len(results)-1
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(content =results[current])

    @commands.command()
    async def gmeaning(self,ctx,*,searchword):
        results = PyDictionary.meaning(searchword)
        embed = discord.Embed(
            color =(discord.Colour.magenta()),
            title = searchword.upper(),
            url =""

       )
        noun =""
        for i in range(len(results['Noun']) if len(results['Noun'])<3 else 3):
            noun+= results['Noun'][i] +',\n'

        verb=''
        for i in range(len(results['Verb']) if len(results['Noun'])<3 else 3):
            verb+= results['Verb'][i] + ',\n'
        embed.set_author(
            name="02 Dictionary",
            icon_url= "https://i.pinimg.com/originals/b7/8a/d8/b78ad8031a4b76a04e7762c550ac4140.png"
        )
        embed.add_field(
           name= "Noun",
           value = noun,
           inline= False
        )
        embed.add_field(
            name= 'Verb',
            value= verb,
            inline=False
        )
        
        print(noun)
        print(verb)

        translation = PyDictionary().translate("happy",'de')

        print(translation)
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Google(client))
    