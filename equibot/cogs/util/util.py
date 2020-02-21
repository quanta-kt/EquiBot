import discord


"""
Utility funtions
"""

async def ensureModeratorOrOwner(ctx, repo):
    """
    Returns true if the sender is a moderator or guild owner.
    Returns false reporting the error otherwise.
    """
    if ctx.author == ctx.guild.owner:
        return True

    moderators = await repo.get_all_mod_roles(ctx.guild.id)
    for mod in moderators:
        if mod in map(lambda role: role.id, ctx.author.roles):
            return True

    await ctx.send("You don't have permission to use this command ;-;")
    return False

async def ensureOwner(ctx):
    """
    Returns True if message author is owner of the guild.
    Returns False reporting the error to the ctx otherwise.
    """
    if ctx.author != ctx.guild.owner:
        await ctx.send("You don't have permission to use this command ;-;")
        return False

    return True

async def ensure_args(ctx, count, args):
    """
    Returns True if len(args) == count,
    Sends the usage message to the `ctx` and returns False otherwise.
    """

    if count != len(args):
        await ctx.send(
            "This is not how you use this command ;-;\n" +
            "**Correct usage:**\n" +
            f"*{ctx.command.usage}*"
        )
        return False

    return True

async def find_channel_by_mention(ctx, toFind):
    """
    Tries to find the channel by mention.
    Sends error if fails, returning None or returns the found channel otherwise
    """
    channel = discord.utils.find(
        lambda channel: channel.mention == toFind,
        ctx.guild.channels
    )

    if channel == None:
        await ctx.send(f"Can't find channel: {toFind} ;-;")

    return channel

    