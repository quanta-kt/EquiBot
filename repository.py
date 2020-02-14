import sqlhelper
import constants
import json

"""
Repository for storage using SQL.
This is basically a bridge between sqlhelper.py and main.py
"""

init = sqlhelper.create_tables

def get_prefix(guild_id):
    prefix = sqlhelper.get_guild_prefix(guild_id)
    
    if prefix == None:
        return constants.DEFAULT_COMMAND_PREFIX
    
    return prefix

def set_prefix(guild_id, new_prefix):
    sqlhelper.update_guild_prefix(guild_id, new_prefix)

def get_bot_token(debug=False):
    """
    Returns the Bot's Token for Auth with Discord.
    Set debug to True when using testing Bot.
    """
    with open('secrets.json') as fp:
        dat = json.load(fp)

        if debug:
            return dat['debug_token']
        else:
            return dat['production_token']

def add_mod_role(guild_id, role_id):
    """
    Adds the moderator role for the gluid to the db.
    Returns False if the role was already present, True otherwise.
    """

    entries = sqlhelper.get_moderator_roles(guild_id)
    if (role_id,) in entries:
        return False

    sqlhelper.add_moderator_role(guild_id, role_id)
    return True

def delete_mod_role(guild_id, to_delete):
    """
    Removes the moderator role for the gluid to from the db.
    Returns False if the role was not present, True otherwise.
    """

    entries = sqlhelper.get_moderator_roles_with_index(guild_id)

    for index, role_id in entries:
        if role_id != to_delete:
            continue

        sqlhelper.delete_moderator_role(index)
        return True

    return False