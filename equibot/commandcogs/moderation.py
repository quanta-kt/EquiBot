from discord.ext import commands
import discord

from .. import util
from .. import repository

class Moderation(commands.Cog):
    """
    Moderation commands.
    """

    def __init__(self, repo: repository.Repository):
        self.repo = repo

    @commands.group()
    async def modrole(self, ctx: commands.Context):
        """
        Add or remove moderator roles.
        action: add/remove
        """

        if ctx.invoked_subcommand == None:
            await ctx.send(
                "**Invalid arguments!**\n" +
                "```Usage:\n" +
                f"{self.repo.get_prefix(ctx.guild.id)}modrole [add | remove] [role to add/remove]```"
            )

    @modrole.command(name='add')
    async def modrole_add(self, ctx: commands.Context, *args):
        if ctx.author != ctx.guild.owner:
            await ctx.send('Only owner can use this command. ;-;')
            return

        if len(args) != 1:
            await ctx.send(
                "**Invalid arguments!**\n" +
                "```" +
                "Usage:\n" +
                f"{self.repo.get_prefix(ctx.guild.id)}modrole [add | remove] [role to add/remove]" +
                "```"
            )

            return

        role = discord.utils.find(
            lambda role: role.name == args[0] or role.mention == args[0],
            ctx.guild.roles
        )

        if role == None:
            await ctx.send(f"Can't find role with name: {args[0]}")
            return

        result = await self.repo.add_mod_role(ctx.guild.id, role.id)

        if result:
            await ctx.send(f'Added moderator role: {role.name}')
        else:
            await ctx.send(f'{role.name} is already moderator!')

    @modrole.command(name='remove')
    async def modrole_remove(self, ctx: commands.Context, *args):
        if ctx.author != ctx.guild.owner:
            await ctx.send('Only owner can use this command. ;-;')
            return

        if len(args) != 1:
            await ctx.send(
                "**Invalid arguments!**\n" +
                "```" +
                "Usage:\n" +
                f"{self.repo.get_prefix(ctx.guild.id)}modrole [add | remove] [role to add/remove]" +
                "```"
            )

            return

        role = discord.utils.find(
            lambda role: role.name == args[0] or role.mention == args[0],
            ctx.guild.roles
        )

        if role == None:
            await ctx.send(f"Can't find role with name: {args[0]}")
            return

        result = await self.repo.delete_mod_role(ctx.guild.id, role.id)

        if result:
            await ctx.send(f'Removed moderator role: {role.name}')
        else:
            await ctx.send(f'{role.name} is not a moderator!')

    @commands.command()
    async def clear(self, ctx: commands.Context, *args):
        """
        Deletes a specified number of messages from the channel.
        Deletes 10 messages if a number was not specified.
        """

        if not await util.isModeratorOrOwner(ctx, self.repo):
            await ctx.send("You're not allowed to issue this command. ;-;")
            return

        n = 10

        if len(args) > 1:
            await ctx.send(
                "**Too many arguments!**" +
                "```" +
                "Usage:\n" +
                f"{self.repo.get_prefix(ctx.guild.id)}" +
                "clear [number of messages]"
                "```"
            )

            return

        if len(args) == 1:
            if not args[0].isnumeric():
                await ctx.send(f"{args[0]} is not a proper number. ;-;")
                return

            n = int(args[0])

        async for message in ctx.channel.history(limit = n + 1): # +1 for command message
            await message.delete()

        notice = await ctx.send(f"Deleted ***{n}*** messages, RIP!")
        await notice.delete(delay=5) #Fades away too! ;)