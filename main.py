#!/usr/bin/python3

from discord.ext import commands
import discord
import constants
import repository

def get_prefix(bot, message):
    return repository.get_prefix(message.channel.guild.id)

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

@bot.command()
async def modrole(ctx: commands.Context, action: str, role: discord.Role):
    """
    Add or remove moderator roles.
    action: add/remove
    """

    action = action.lower()

    if action == 'add':
        result = repository.add_mod_role(ctx.guild.id, role.id)

        if result:
            await ctx.send(f'Added moderator role: {role.name}')
        else:
            await ctx.send(f'{role.name} is already moderator!')

    elif action == 'remove':
        result = repository.delete_mod_role(ctx.guild.id, role.id)

        if result:
            await ctx.send(f'Removed moderator role: {role.name}')
        else:
            await ctx.send(f'{role.name} is not a moderator!')

repository.init()
bot.run(repository.get_bot_token(True))
