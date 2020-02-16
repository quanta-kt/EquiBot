import json

from . import sqlhelper
from . import constants

"""
Repository for storage using SQL.
This is basically a bridge between sqlhelper and app
"""

class Repository:

    def __init__(self, sql_file=constants.DATBASE_FILE):
        self.sql = sqlhelper.SqlHelper(sql_file)

    def get_prefix(self, guild_id):
        prefix = self.sql.get_guild_prefix(guild_id)

        if prefix == None:
            return constants.DEFAULT_COMMAND_PREFIX

        return prefix

    def set_prefix(self, guild_id, new_prefix):
        self.sql.update_guild_prefix(guild_id, new_prefix)

    def get_bot_token(self, debug=False):
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

    def add_mod_role(self, guild_id, role_id):
        """
        Adds the moderator role for the gluid to the db.
        Returns False if the role was already present, True otherwise.
        """

        entries = self.sql.get_moderator_roles(guild_id)
        if (role_id,) in entries:
            return False

        self.sql.add_moderator_role(guild_id, role_id)
        return True

    def delete_mod_role(self, guild_id, to_delete):
        """
        Removes the moderator role for the gluid to from the db.
        Returns False if the role was not present, True otherwise.
        """

        entries = self.sql.get_moderator_roles_with_index(guild_id)

        for index, role_id in entries:
            if role_id != to_delete:
                continue

            self.sql.delete_moderator_role(index)
            return True

        return False

    def get_all_mod_roles(self, guild_id):
        """
<<<<<<< HEAD
        Returns map of all role IDs registered as moderator.
        """
        
        return map(
            lambda t : t[0],
            self.sql.get_moderator_roles(guild_id)
=======
        Returns list of all role IDs registered as moderator.
        """
        
<<<<<<< HEAD
        return list(
            map(
                lambda t : t[0],
                self.sql.get_moderator_roles(guild_id)
            )
>>>>>>> Fix permission checks (#11)
=======
        return map(
            lambda t : t[0],
            self.sql.get_moderator_roles(guild_id)
>>>>>>> Move modrole actions to sub-commands
        )
