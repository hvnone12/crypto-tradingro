from discord.ext import commands
import asyncio


class Cleaner:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_server=True)
    async def clean(self, ctx, lines: int=80000):
        """<number of line> (everything if no number)"""
        # Removes the lines
        async for message in self.bot.logs_from(ctx.message.channel, limit=lines):
            await self.bot.delete_message(message)
        # Auto-remove message
        temp_message = await self.bot.send_message(ctx.message.channel, 'Cleaned!')
        await asyncio.sleep(5)
        await self.bot.delete_message(temp_message)


def setup(bot: commands.Bot):
    bot.add_cog(Cleaner(bot))
