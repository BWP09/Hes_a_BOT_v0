from discord.ext import commands

bot = commands.Bot(command_prefix='$')

TOKEN = "OTQ3MzQzMTg5MzUyNzk2MjIw.Yhr4GQ.l0_hf-1Usl0ajqqYQW2X4XiJdc8"

@bot.command()
async def test(ctx):
    await ctx.channel.send('test')

bot.run(TOKEN)