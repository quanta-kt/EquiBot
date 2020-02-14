#!/usr/bin/python3

from discord.ext import commands
import constants
import repository

def get_prefix(bot, message):
    ret = repository.get_prefix(message.channel.guild.id)
    print(ret)
    print("ddd")
    return ret

bot = commands.Bot(command_prefix=get_prefix, description="""General purpose bot for Eqvivalent.""")

@bot.event
async def on_ready():
    print("Bot online.")

@bot.command()
async def prefix(ctx, new_prefix):
    """
    Changes the prefix for the bot in your server.
    """

    if (ctx.author == ctx.guild.owner):
        repository.set_prefix(ctx.message.channel.guild.id, new_prefix)
    else:
        await ctx.send("You are not allowed to change the prefix. ;-;")
        return

    await ctx.send('Prefix set to: "{}"'.format(new_prefix))

@bot.command
async def modrole(ctx, action, role):
    """
    Add or remove moderator roles.
    action: add/remove
    """
    #TODO: Implement!
    pass

repository.init()
bot.run(repository.get_bot_token(True))
