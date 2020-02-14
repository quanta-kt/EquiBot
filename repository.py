import sqlhelper
import constants
import json

"""
Repository for storage using SQL.
This is basically a bridge between sqlhelper.py and main.py
"""

init = sqlhelper.init_prefix_table

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