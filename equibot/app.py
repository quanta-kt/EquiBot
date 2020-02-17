#!/usr/bin/python3

from discord.ext import commands
import discord
import asyncio

from . import constants
from . import repository
from . import util

bot = commands.Bot(
    command_prefix = lambda bot, message:
            repo.get_prefix(message.channel.guild.id),

    description="""General purpose bot for Eqvivalent."""
)

repo = None #Initiated in `on_ready()`

@bot.event
async def on_ready():
    print("Bot online.")
    global repo
    repo = await repository.Repository.create()

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

@bot.command()
async def prefix(ctx, *args):
    """
    Changes the prefix for the bot in your server.
    """

    if len(args) != 1:
        await ctx.send(
            "**Invalid arguments**\n" +
            "```" +
            "Usage:\n" +
            f"{repo.get_prefix(ctx.guild.id)}prefix [new prefix]"
            "```"
        )
        
        return

    new_prefix = args[0]

    isModerator = discord.utils.find(
        lambda modrole: modrole in ctx.author.roles,
        await repo.get_all_mod_roles(ctx.guild.id)
    ) != None

    if not (ctx.author == ctx.guild.owner or isModerator):
        await ctx.send("You are not allowed to change the prefix. ;-;")
        return

    await repo.set_prefix(ctx.guild.id, new_prefix)
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
async def modrole_add(ctx: commands.Context, *args):
    if ctx.author != ctx.guild.owner:
        await ctx.send('Only owner can use this command. ;-;')
        return

    if len(args) != 1:
        await ctx.send(
            "**Invalid arguments!**\n" +
            "```" +
            "Usage:\n" +
            f"{repo.get_prefix(ctx.guild.id)}modrole [add | remove] [role to add/remove]" +
            "```"
        )

        return

    role = discord.utils.find(
        lambda role: role.name == args[0] or role.mention == args[0],
        ctx.guild.roles
    )

    if role == None:
        await ctx.send(f"Can't find role with name: {args[0]}")
        return

    result = await repo.add_mod_role(ctx.guild.id, role.id)

    if result:
        await ctx.send(f'Added moderator role: {role.name}')
    else:
        await ctx.send(f'{role.name} is already moderator!')

@modrole.command(name='remove')
async def modrole_remove(ctx: commands.Context, *args):
    if ctx.author != ctx.guild.owner:
        await ctx.send('Only owner can use this command. ;-;')
        return

    if len(args) != 1:
        await ctx.send(
            "**Invalid arguments!**\n" +
            "```" +
            "Usage:\n" +
            f"{repo.get_prefix(ctx.guild.id)}modrole [add | remove] [role to add/remove]" +
            "```"
        )

        return

    role = discord.utils.find(
        lambda role: role.name == args[0] or role.mention == args[0],
        ctx.guild.roles
    )

    if role == None:
        await ctx.send(f"Can't find role with name: {args[0]}")
        return
    
    result = await repo.delete_mod_role(ctx.guild.id, role.id)

    if result:
        await ctx.send(f'Removed moderator role: {role.name}')
    else:
        await ctx.send(f'{role.name} is not a moderator!')

@bot.command()
async def clear(ctx: commands.Context, *args):
    """
    Deletes a specified number of messages from the channel.
    Deletes 10 messages if a number was not specified.
    """

    if not await util.isModeratorOrOwner(ctx, repo):
        await ctx.send("You're not allowed to issue this command. ;-;")
        return

    n = 10

    if len(args) > 1:
        await ctx.send(
            "**Too many arguments!**" +
            "```" +
            "Usage:\n" +
            f"{repo.get_prefix(ctx.guild.id)}" +
            "clear [number of messages]"
            "```"
        )

        return

    if len(args) == 1:
        if not args[0].isnumeric():
            await ctx.send(f"{args[0]} is not a proper number. ;-;")
            return

        n = int(args[0])

    async for message in ctx.channel.history(limit = n + 1): # +1 for command message
        await message.delete()

    notice = await ctx.send(f"Deleted ***{n}*** messages, RIP!")
    await notice.delete(delay=5) #Fades away too! ;)

def main(debug=False):
    bot.run(repository.get_bot_token(debug))

if __name__ == '__main__':
    main()
