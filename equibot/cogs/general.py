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

            curr_time = time.time()
            filtered = []

            for timer in self.timers:
                finish_time = timer[0]
                ctx = timer[1]

                if finish_time <= curr_time:
                    await ctx.send(f"{ctx.author.mention} Your timer is done!")
                else:
                    filtered.append(timer)

            self.timers = filtered #Forget about timers that are done
            await asyncio.sleep(1)

    @commands.command(usage='timer [time in sec |  Xh Xm Xs]')
    async def timer(self, ctx: commands.Context, *args):
        """
        Sets a timer. You'll get pinged when the timer finishes!
        """

        print(f'Command {ctx.command.name} from guild {ctx.guild.name}')

        if len(args) == 0:
            await ctx.send(
                "Incorrect usage ;-;\n"
                "I expect atleast one parameter."
            )

            return

        finish_time = 0

        for token in args:

            if token.isnumeric():
                finish_time += int(token)
                continue

            val = token[:-1]
            unit = token[-1].lower()

            if not val.isnumeric():
                await ctx.send(f"*{val}* was expected to be a numeric value. ;-;")
                return

            val = int(val)

            if unit == 's':
                finish_time += val
            elif unit == 'm':
                finish_time += (val * 60)
            elif unit == 'h':
                finish_time += (val * 60 * 60)
            else:
                await ctx.send(
                    f"Unknown time unit: {unit}\n" +
                    "Valid options are: h, m, s"
                )

                return

        self.timers.append((finish_time + time.time(), ctx))
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
