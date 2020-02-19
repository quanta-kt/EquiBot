"""
Utility funtions
"""

async def isModeratorOrOwner(ctx, repo):
    """
    Returns true if the sender is a moderator or guild owner
    """
    if ctx.author == ctx.guild.owner:
        return True
    moderators = await repo.get_all_mod_roles(ctx.guild.id)
    for mod in moderators:
        if mod in map(lambda role: role.id, ctx.author.roles):
            return True
    return False

def isOwner(ctx):
    """
    Returns true of sender is the server owner.
    """
    return ctx.author == ctx.guild.owner