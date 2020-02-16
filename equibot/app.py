#!/usr/bin/python3

from discord.ext import commands
import discord

from . import constants
from . import repository

bot = commands.Bot(
    command_prefix = lambda bot, message : repo.get_prefix(message.channel.guild.id),
    description="""General purpose bot for Eqvivalent."""
)

repo = repository.Repository()

@bot.event
async def on_ready():
    print("Bot online.")

@bot.command()
async def prefix(ctx, new_prefix):
    """
    Changes the prefix for the bot in your server.
    """

    if (ctx.author == ctx.guild.owner):
        repo.set_prefix(ctx.message.channel.guild.id, new_prefix)
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
        result = repo.add_mod_role(ctx.guild.id, role.id)

        if result:
            await ctx.send(f'Added moderator role: {role.name}')
        else:
            await ctx.send(f'{role.name} is already moderator!')

    elif action == 'remove':
        result = repo.delete_mod_role(ctx.guild.id, role.id)

        if result:
            await ctx.send(f'Removed moderator role: {role.name}')
        else:
            await ctx.send(f'{role.name} is not a moderator!')

def main(debug=False):
    bot.run(repo.get_bot_token(debug))

if __name__ == '__main__':
    main()
