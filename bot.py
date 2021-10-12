
import discord
from discord.ext import commands
import random
import os

client = commands.Bot(command_prefix='*')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game('Appadi Podu Podu'))
    print('Bot is Ready')

@client.event
async def on_member_join(ctx,member):
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! {round(client.latency * 1000)}ms')

@client.command()
async def sayloveyou(ctx):
    await ctx.send(f'Fuck You 💩{ctx.message.author.mention}')

@client.command(aliases =['8ball','test'])
async def _8ball(ctx,*,question):
    response =[
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]


    await ctx.send(f'{random.choice(response)}')


@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)


@client.command()
async def avatar(ctx, member:discord.Member):
    userAvatar = member.avatar_url
    embed = discord.Embed(
        colour =(discord.Colour.magenta()),
        title = member.display_name,
    )
    embed.set_image(url=userAvatar)
    await ctx.send(embed = embed)


@client.command()
async def disconnect(ctx, member:discord.Member):
    await ctx.send(f'{member.mention} disconnected successfully')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('ODk0NTA2Nzk1MDk0MTM0Nzg0.YVrAXw.u3s4DYwBlg80sZyvLx_F7X0fpKc')