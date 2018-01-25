from discord.ext import commands
import discord
import asyncio
import utils.data as data


class Greeter:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def on_member_join(self, member: discord.Member):
        # Greetings	
        welcome_channel = self.bot.get_channel('399674110348886016')

        membru = discord.utils.get(data.server.roles, name='Membru')
        msg = await self.bot.send_message(welcome_channel, '{}, Bine ai venit pe Crypto-Trading Romania! Îți urăm '
                                                           'succes și sperăm să ai profit cât mai mult! '
                                                           ':wink::moneybag::money:'.format(member.mention))
        await self.bot.add_roles(member, membru)


def setup(bot: commands.Bot):
    bot.add_cog(Greeter(bot))
