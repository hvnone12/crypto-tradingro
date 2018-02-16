import discord
import utils.data as data
from utils.roles import get_role, get_next_role, get_previous_role, roles
from discord.ext import commands
import discord.errors
import asyncio


class Roles:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    	
    @commands.command(pass_context=True)
    async def update(self, ctx: commands.Context):
        update_channel = self.bot.get_channel('413954987446632449')
        member = ctx.message.author
        role = discord.utils.get(ctx.message.server.roles, name='Update')
        msg = await self.bot.send_message(update_channel, '{}, de acum vei fi anuntat cand apar informatii noi!'
                                                           ':white_check_mark:'.format(member.mention))
        await self.bot.add_roles(member, role)


    @commands.command(pass_context=True)
    async def noupdate(self, ctx: commands.Context):
        update_channel = self.bot.get_channel('413954987446632449')
        member = ctx.message.author
        role = discord.utils.get(ctx.message.server.roles, name='Update')
        msg = await self.bot.send_message(update_channel, '{}, de acum nu vei mai fi anuntat cand apar informatii noi!'
                                                           ':negative_squared_cross_mark:'.format(member.mention))
        await self.bot.remove_roles(member, role)

    @commands.command(pass_context=True)
    async def invitatii(self, ctx):
        """Shows the invites, only in invite-counter"""
        author = ctx.message.author
        if not ctx.message.channel.id == '401435705668009985':
            await self.bot.delete_message(ctx.message)
            return
        has_rank = False
        msg = None
        msg2 = None
        for user_invite in data.users_invites.values():
            if user_invite[0].id == author.id:
                msg = await self.bot.say('<@{}>, ai {} invitații acceptate!'.format(user_invite[0].id, user_invite[1]))
                next_rank, invites_needed = get_next_role(user_invite[1])
                msg2 = await self.bot.say(
                    '<@{}>,  mai ai nevoie de încă {} invitații pentru a avansa la {}!'.format(user_invite[0].id,
                                                                                              invites_needed -
                                                                                              user_invite[1],
                                                                                              next_rank))
                has_rank = True
        if not has_rank:
            msg = await self.bot.say('<@{}>, nu ai nicio invitație acceptată!'.format(ctx.message.author.id))
            msg2 = await self.bot.say(
                '<@{}>, mai ai nevoie de o invitație pentru a deveni Rank 10!'.format(ctx.message.author.id))

    @commands.command(pass_context=True)
    async def rank(self, ctx):
        if not ctx.message.channel.id == '401435705668009985':
            await self.bot.delete_message(ctx.message)
            return
        """Shows the roles affiliate level"""
        message = ''
        for invites, rank in roles.items():
            message += '**{}** - {} invites\n'.format(rank, invites)
        embed = discord.Embed(title='Rank', description=message, color=0xfff71e)
        msg = await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def members(self, ctx):
        if not ctx.message.channel.id == '401435705668009985':
            await self.bot.delete_message(ctx.message)
            return
        """Shows somse info"""
        everyone = data.server.members
        members = list(filter(lambda x: not x.bot, everyone))
        online_members = list(filter(lambda x: x.status.value == 'online', members))
        embed = discord.Embed(title='Membri Server', description='------------------\n''**Membri Online:** {}'
                                                                  '\n**Total membri:** {}'
                              .format(online_members.__len__(), members.__len__()), color=0xfff71e)
        msg = await self.bot.send_message(ctx.message.channel, embed=embed)


async def rli(bot):
    # Get the current invites
    while not bot.is_closed:

        await asyncio.sleep(35)
        # Check if server is ready and registered
        if data.server is None:
            continue
        current_invites = await bot.invites_from(data.server)
        for invite in current_invites:
            try:
                # User inviter
                print(invite)
                inviter = invite.inviter
                if inviter.id not in data.users_invites:
                    data.users_invites[inviter.id] = [inviter, 0]
                if invite.id not in data.invites:
                    data.invites[invite.id] = invite
                    data.users_invites[inviter.id][1] += invite.uses
                else:
                    old_uses = data.invites[invite.id].uses
                    difference = invite.uses - old_uses
                    data.invites[invite.id] = invite
                    data.users_invites[inviter.id][1] += difference
            except:
                pass
        await assign_roles(bot)


async def assign_roles(bot):
    await asyncio.sleep(5)
    # Check if server is ready and registered
    if data.server is None:
        return
    print('Setting roles...')
    for user_invite in data.users_invites.values():

        # Get stored data
        user = user_invite[0]

        invites = user_invite[1]
        # Set the role
        member = discord.utils.get(data.server.members, name=user.name)
        if member is None:
            continue
        if member.top_role.name == 'Admin':
            print('I will not change the role for admins')
            continue

        role = discord.utils.get(data.server.roles, name='Developer')
        if role in member.roles:
            continue

        if member.top_role.name == 'Developer':
            print('I will not change the role for mods')
            continue

        role = discord.utils.get(data.server.roles, name='Premium')
        if role in member.roles:
            continue

        if member.top_role.name == 'Premium':
            print('I will not change the role for Advisory')
            continue

        role = discord.utils.get(data.server.roles, name='VIP')
        if role in member.roles:
            continue

        if member.top_role.name == 'VIP':
            print('I will not change the role for VIP')
            continue

        role = discord.utils.get(data.server.roles, name='Founder, CEO')
        if role in member.roles:
            continue

        if member.top_role.name == 'Founder, CEO':
            print('I will not change the role for CEO')
            continue

        role = discord.utils.get(data.server.roles, name='Admin')
        if role in member.roles:
            continue

        if member.top_role.name == 'Administrator':
            print('I will not change the role for Admin')
            continue

        # Get the proper role based on invites
        role_name = get_role(invites)
        if member.top_role.name == role_name or member.top_role.name == 'Admin':
            continue
        role = discord.utils.get(data.server.roles, name=role_name)
        if role is None:
            continue
        print('{} with {} invites. Role -> {}'.format(user.display_name, invites, role.name))
        try:
            await bot.add_roles(member, role)
        except discord.errors.Forbidden as e:
            pass
        await asyncio.sleep(0.1)


def setup(bot: commands.Bot):
    bot.add_cog(Roles(bot))
    bot.loop.create_task(rli(bot))
