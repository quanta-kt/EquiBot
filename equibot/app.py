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

    #Checks if one of sender's roles is a registered moderator role
    def hasModRole():
        modroles = repo.get_all_mod_roles(ctx.guild.id)
        for role in ctx.author.roles:
            if role.id in modroles:
                return True
        return False

    if not (ctx.author == ctx.guild.owner or hasModRole()):
        await ctx.send("You are not allowed to change the prefix. ;-;")
        return

    repo.set_prefix(ctx.guild.id, new_prefix)
    await ctx.send('Prefix set to: "{}"'.format(new_prefix))

@bot.group()
async def modrole(ctx: commands.Context):
    """
    Add or remove moderator roles.
    action: add/remove
    """

    if ctx.invoked_subcommand == None:
        await ctx.send(
            "**Invalid arguments!**\n" +
            "```Usage:\n" +
            f"{repo.get_prefix(ctx.guild.id)}modrole [add | remove] [role to add/remove]```"
        )

@modrole.command(name='add')
async def modrole_add(ctx: commands.Context, role: discord.Role):
    if ctx.author.id != ctx.guild.owner.id:
        await ctx.send('Only owner can use this command. ;-;')
        return

    result = repo.add_mod_role(ctx.guild.id, role.id)

    if result:
        await ctx.send(f'Added moderator role: {role.name}')
    else:
        await ctx.send(f'{role.name} is already moderator!')

@modrole.command(name='remove')
async def modrole_remove(ctx: commands.Context, role: discord.Role):
    if ctx.author.id != ctx.guild.owner.id:
        await ctx.send('Only owner can use this command. ;-;')
        return
    
    result = repo.delete_mod_role(ctx.guild.id, role.id)

    if result:
        await ctx.send(f'Removed moderator role: {role.name}')
    else:
        await ctx.send(f'{role.name} is not a moderator!')

def main(debug=False):
    bot.run(repo.get_bot_token(debug))

if __name__ == '__main__':
    main()
