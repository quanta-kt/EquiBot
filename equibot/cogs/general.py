from discord.ext import commands
import discord
import asyncio
import time

from . import util
from .. import repository

class General(commands.Cog):
    """
    General purpose utility commands
    """

    def __init__(self, bot, repo: repository.Repository):
        self.repo = repo
        self.timers = []
        self.bot = bot
        bot.loop.create_task(self.timer_tick())

    @commands.command(usage='prefix [new_prefix]')
    async def prefix(self, ctx :commands.Context, *args):
        """
        Changes the prefix for the bot in your server.
        """

        print(f'Command {ctx.command.name} from guild {ctx.guild.name}')

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

        print(f'Command {ctx.command.name} from guild {ctx.guild.name}')

        reason =  ' '.join(reason)
        if reason.isspace() or reason == '':
            reason = "No reason provided."

        await self.repo.set_afk_status(ctx.guild.id, ctx.author.id, reason)
        await ctx.send(
            embed = util.simpleEmbed(
                f"Goodbye {ctx.author.display_name}!",
                "**I've set your AFK status to:**\n" +
                reason
            )
        )

    async def timer_tick(self):
        while True:

            filtered = []

            for timer in self.timers:
                finish_time = timer[0]
                ctx = timer[1]

                if finish_time <= time.time():
                    await ctx.send(f"{ctx.author.mention} Your timer is done!")
                else:
                    filtered.append(timer)

            self.timers = filtered #Forget about timers that are done
            await asyncio.sleep(1)

    @commands.command(usage='timer [time in sec]')
    async def timer(self, ctx: commands.Context, *args):
        """
        Sets a timer. You'll get pinged when the timer finishes!
        """

        print(f'Command {ctx.command.name} from guild {ctx.guild.name}')

        if not await util.ensure_args(ctx, 1, args):
            return

        if not args[0].isnumeric():
            await ctx.send("I expect numbers there ;-;")
            return

        finish_time = time.time() + int(args[0])
        self.timers.append(
            (finish_time, ctx)
        )

        await ctx.message.add_reaction("⏰")

    @commands.command(usage='timercancel')
    async def timercancel(self, ctx: commands.Context):
        """
        Cancel all your pending timers in the current channel.
        """

        self.timers = [
            timer
            for timer in self.timers
            if timer[1].author != ctx.author or timer[1].channel != ctx.channel
        ]

        await ctx.message.add_reaction("✅")
