#!/usr/bin/python3

from discord.ext import commands
import discord

from . import repository
from . import cogs
from .message_actions import MessageActions

repo = repository.Repository()

bot = commands.Bot(
    command_prefix = lambda bot, message:
        repo.get_prefix(message.guild.id),

    description="""A nice general purpose bot for your server"""
)

actions = MessageActions(bot, repo)

#Register COGs
bot.add_cog(cogs.General(repo))
bot.add_cog(cogs.Moderation(repo))

birthdayscog = cogs.Birthdays(repo)
bot.add_cog(birthdayscog)

@bot.event
async def on_ready():
    print("Bot online.")
    await bot.change_presence(activity=discord.Game(name="Ping for help!"))
    bot.loop.create_task(birthdayscog.birthday_ticker(bot))

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    await actions.invoke(message)
    await bot.process_commands(message)

def main(debug=False):
    bot.run(repo.get_bot_token(debug))

if __name__ == '__main__':
    main()
