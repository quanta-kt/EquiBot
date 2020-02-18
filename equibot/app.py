#!/usr/bin/python3

from discord.ext import commands

from . import repository
from . import commandcogs

bot = commands.Bot(
    command_prefix = lambda bot, message:
            repo.get_prefix(message.channel.guild.id),

    description="""A nice general purpose bot for your server"""
)

repo = None #Initiated in `on_ready()`

@bot.event
async def on_ready():
    print("Bot online.")
    global repo
    repo = await repository.Repository.create()

    #Register COGs
    bot.add_cog(commandcogs.General(repo))
    bot.add_cog(commandcogs.Moderation(repo))

@bot.event
async def on_message(message):

    if bot.user.mentioned_in(message) and not message.mention_everyone:
        #We have got a mention!
        prefix = repo.get_prefix(message.guild.id)
        await message.add_reaction('👀')
        await message.channel.send(
            f"My prefix here is: **{prefix}**\n" +
            f"Try **{prefix}help** to get list of commands!"
        )

    await bot.process_commands(message)

def main(debug=False):
    bot.run(repository.get_bot_token(debug))

if __name__ == '__main__':
    main()
