from discord.ext import commands
import discord
import asyncio
import utils.data as data


class Update:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def on_message(self, message, member: discord.Member):
	
        update_channel = self.bot.get_channel('413954987446632449')
		update = discord.utils.get(data.server.roles, name='Update')
		if message.content.startswith('!update'):
        msg = await self.bot.send_message(update_channel, '{}, De acum vei fi anuntat cand apar informatii noi!'
                                                           ':money_mouth::moneybag::money_with_wings:'.format(member.mention))
        await self.bot.add_roles(member, update)


def setup(bot: commands.Bot):
    bot.add_cog(Update(bot))
