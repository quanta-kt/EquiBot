from discord.ext import commands
import discord

from . import util
from .. import repository

class General(commands.Cog):
    """
    General purpose utility commands
    """

    def __init__(self, repo: repository.Repository):
        self.repo = repo

    @commands.command(usage='prefix [new_prefix]')
    async def prefix(self, ctx :commands.Context, *args):
        """
        Changes the prefix for the bot in your server.
        """

        if not await util.ensure_args(ctx, 1, args):
            return

        new_prefix = args[0]

        if not await util.ensureOwner(ctx):
            await ctx.send("You are not allowed to change the prefix. ;-;")
            return

        await self.repo.set_prefix(ctx.guild.id, new_prefix)
        await ctx.send('Prefix set to: "{}"'.format(new_prefix))

    @commands.command(usage='bye [reason...]')
    async def bye(self, ctx: commands.Context, *reason):
        """
        Set your AFK status.
        People who mention you will get notice of you being AFK.
        """

        reason =  ' '.join(reason)
        if reason.isspace() or reason == '':
            reason = "No reason provided."

        await self.repo.set_afk_status(ctx.guild.id, ctx.author.id, reason)
        await ctx.send(
            f"**Goodbye {ctx.author.display_name}!** \n" +
            "I've set your AFK status to:\n" +
            reason
        )