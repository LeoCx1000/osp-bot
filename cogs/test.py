import discord, asyncio, typing, datetime
from discord.ext import commands, menus

class test(commands.Cog):
    """๐งช Test commands. ๐ May not work or not be what you think they'll be."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="๐๐๐")
    @commands.cooldown(1, 5.0, commands.BucketType.channel)
    async def blink(self, ctx):
        msg = await ctx.send("๐๐๐")
        await asyncio.sleep(0.5)
        await msg.edit(content="โ๐โ")
        await asyncio.sleep(0.1)
        await msg.edit(content="๐๐๐")
        await asyncio.sleep(1)
        await msg.delete()
        await ctx.message.delete()

    @commands.command(help="๐")
    @commands.cooldown(1, 5.0, commands.BucketType.channel)
    async def blink2(self, ctx):
        msg = await ctx.send("๐")
        await asyncio.sleep(0.5)
        await msg.edit(content="๐")
        await asyncio.sleep(0.1)
        await msg.edit(content="๐")
        await asyncio.sleep(1)
        await msg.delete()
        await ctx.message.delete()

    @commands.command(help="๐๐๐")
    @commands.cooldown(1, 5.0, commands.BucketType.channel)

    async def wink(self, ctx):
        msg = await ctx.send("๐๐๐")
        await asyncio.sleep(0.5)
        await msg.edit(content="๐๐โ")
        await asyncio.sleep(0.1)
        await msg.edit(content="๐๐๐")
        await asyncio.sleep(1)
        await msg.delete()
        await ctx.message.delete()

    @commands.command(help="hmm")
    @commands.cooldown(1, 5.0, commands.BucketType.channel)
    async def smiles(self, ctx):
        msg = await ctx.send(":slight_smile:")
        await asyncio.sleep(1)
        await msg.edit(content=":grinning:")
        await asyncio.sleep(1)
        await msg.edit(content=":smiley:")
        await asyncio.sleep(1)
        await msg.edit(content=":smile:")
        await asyncio.sleep(1)
        await msg.edit(content=":grin:")
        await asyncio.sleep(1)
        await msg.edit(content=":laughing:")
        await asyncio.sleep(1)
        await msg.edit(content=":joy:")
        await asyncio.sleep(1)
        await msg.edit(content=":rofl:")
        await asyncio.sleep(1)
        await msg.delete()
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(test(bot))
