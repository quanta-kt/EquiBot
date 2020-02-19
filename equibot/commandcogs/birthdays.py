from discord.ext import commands
import discord
import asyncio

from .. import util
from .. import repository

class Birthdays(commands.Cog):

    def __init__(self, repo: repository.Repository):
        self.repo = repo

    @commands.command()
    async def birthday(self, ctx: commands.Context, *args):
        """
        Add your name to birthday calendar!
        """

        if len(args) != 2:
            await ctx.send(
                "Invalid arguments ;-;\n" +
                "**Usage: " +
                f"{self.repo.get_prefix(ctx.guild.id)}**" +
                "birthday [month] [day]"
            )

            return

        month, day = None, None

        if not args[0].isnumeric() or (month := int(args[0])) > 12:
            await ctx.send(f"Does {args[0]} looks like a month number to you? ;-;")
            return

        if not args[1].isnumeric() or (day := int(args[1])) > 31:
            await ctx.send(f"Does {args[1]} looks like a day of a month to you? ;-;")
            return

        await self.repo.set_birthdate(ctx.author.id, month, day)
        await ctx.send(
            "Awesome!\n" + 
            "We will remember you birthday\n" +
            "UmU"
        )
    
    @commands.command(name="birthday-setup")
    async def birthday_setup(self, ctx: commands.Context, *args):
        """
        Set-up birthday calendar for server!
        """

        if len(args) != 2:
            await ctx.send(
                "Invalid arguments ;-;\n" +
                "**Usage: " +
                f"{self.repo.get_prefix(ctx.guild.id)}**" +
                "birthday-setup [channel for calendar] [channel for greets]"
            )

            return

        if not util.isOwner(ctx):
            await ctx.send("You don't have permission to issue this command. ;-;")
            return

        class NotFoundError(Exception): pass

        async def find_channel_or_raise(toFind):
            result = discord.utils.find(
                lambda channel: channel.mention == toFind,
                ctx.guild.channels
            )

            if result == None:
                await ctx.send(f"Can't find channel: {toFind} ;-;")
                raise NotFoundError()
            return result

        try:
            calendar_channel = await find_channel_or_raise(args[0])
            greet_channel = await find_channel_or_raise(args[1])

            await self.repo.set_birthday_channels(
                ctx.guild.id,
                calendar_channel.id,
                greet_channel.id
            )

            await ctx.send(
                "Awesome!\n" +
                "I've set it up as follows:\n" +
                f"**Bithday calendar at:** {calendar_channel.mention}\n" +
                f"**Greetings at:** {greet_channel.mention}\n" +
                ":3"
            )

        except NotFoundError:
            return

    async def greet_birthday(self, channel, member):
        await channel.send(f"Happy birthday {member.mention}!")

    async def birthday_ticker(self, bot: commands.Bot):
        while True:

            if await self.repo.has_greeted_today():
                print("Sleeping for long time")
                await asyncio.sleep(15)
                continue

            birthdays = list(await self.repo.get_birthday_kids())

            if birthdays != None:
                for guild in bot.guilds:
                    if (channel_ids := await self.repo.get_birthday_channels(guild.id)) != None:
                        channel = guild.get_channel(channel_ids[1])

                        for kid_id in birthdays:
                            if kid_id in map(lambda member: member.id, guild.members):
                                await self.greet_birthday(channel, guild.get_member(kid_id))
                                
                    else: print(f"Birthday channels not setup for guild: '{guild.name}' id: {guild.id}")

                await self.repo.update_greet_completion_date()
                print("Birthdays concluded.")

            else:
                print("No birthdays today.")
                await self.repo.update_greet_completion_date()

            await asyncio.sleep(5)
