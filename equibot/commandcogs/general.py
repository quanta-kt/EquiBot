from discord.ext import commands
import discord

from .. import repository

class General(commands.Cog):
    """
    General purpose utility commands
    """

    def __init__(self, repo: repository.Repository):
        self.repo = repo

    @commands.command()
    async def prefix(self, ctx :commands.Context, *args):
        """
        Changes the prefix for the bot in your server.
        """

        if len(args) != 1:
            await ctx.send(
                "**Invalid arguments**\n" +
                "```" +
                "Usage:\n" +
                f"{self.repo.get_prefix(ctx.guild.id)}prefix [new prefix]"
                "```"
            )

            return

        new_prefix = args[0]

        isModerator = discord.utils.find(
            lambda modrole: modrole in ctx.author.roles,
            await self.repo.get_all_mod_roles(ctx.guild.id)
        ) != None

        if not (ctx.author == ctx.guild.owner or isModerator):
            await ctx.send("You are not allowed to change the prefix. ;-;")
            return

        await self.repo.set_prefix(ctx.guild.id, new_prefix)
        await ctx.send('Prefix set to: "{}"'.format(new_prefix))

    @commands.command()
    async def bye(self, ctx: commands.Context, *reason):
        """
        Set your AFK status.
        People who mention you will get notice of you being AFK.
        """

        reason =  ' '.join(reason)
        await self.repo.set_afk_status(ctx.guild.id, ctx.author.id, reason)
        await ctx.send(
            f"**Goodbye {ctx.author.display_name}!**\n**" +
            "I've set your AFK status to:\n" +
            f"*{reason}*"
        )