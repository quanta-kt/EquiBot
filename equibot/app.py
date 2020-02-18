#!/usr/bin/python3

from discord.ext import commands
import discord

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
async def on_message(message: discord.Message):

    if bot.user.mentioned_in(message) and not message.mention_everyone:
        #We have got a mention!
        prefix = repo.get_prefix(message.guild.id)
        await message.add_reaction('👀')
        await message.channel.send(
            f"My prefix here is: **{prefix}**\n" +
            f"Try **{prefix}help** to get list of commands!"
        )

    if (await repo.get_afk_status(message.guild.id, message.author.id)) != None:
        await repo.clear_afk_status(message.guild.id, message.author.id)
        await message.channel.send(
            f"**Welcome back {message.author.display_name}!\n" +
            "I've removed your AFK status"
        )

    for user in message.mentions:
        afk_status = await repo.get_afk_status(message.guild.id, user.id)
        if afk_status == None:
            return

        await message.channel.send(
            f"Nice, but {user.display_name} is AFK.\n" +
            f"**Reason:** {afk_status}"
        )

    await bot.process_commands(message)

def main(debug=False):
    bot.run(repository.get_bot_token(debug))

if __name__ == '__main__':
    main()
