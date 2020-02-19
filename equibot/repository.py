import json
import datetime

from . import sqlhelper
from . import constants

#This is left as non-async for a purose
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

class Repository:
    """
    Repository for storage using SQL.
    This is basically a bridge between sqlhelper and app
    """

    @classmethod
    async def create(cls, sql_file=constants.DATBASE_FILE):
        repo = Repository()
        repo.sql = await sqlhelper.SqlHelper.create(sql_file)
        return repo

    #This function isn't async because we need to use it
    #outside the coroutines
    def get_prefix(self, guild_id):
        prefix = self.sql.get_guild_prefix(guild_id)

        if prefix == None:
            return constants.DEFAULT_COMMAND_PREFIX

        return prefix

    async def set_prefix(self, guild_id, new_prefix):
        await self.sql.update_guild_prefix(guild_id, new_prefix)

    async def add_mod_role(self, guild_id, role_id):
        """
        Adds the moderator role for the gluid to the db.
        Returns False if the role was already present, True otherwise.
        """

        entries = await self.sql.get_moderator_roles(guild_id)
        if (role_id,) in entries:
            return False

        await self.sql.add_moderator_role(guild_id, role_id)
        return True

    async def delete_mod_role(self, guild_id, to_delete):
        """
        Removes the moderator role for the gluid to from the db.
        Returns False if the role was not present, True otherwise.
        """

        entries = await self.sql.get_moderator_roles_with_index(guild_id)

        for index, role_id in entries:
            if role_id != to_delete:
                continue

            await self.sql.delete_moderator_role(index)
            return True

        return False

    async def get_all_mod_roles(self, guild_id):
        """
        Returns map of all role IDs registered as moderator.
        """
        
        return map(
            lambda t : t[0],
            await self.sql.get_moderator_roles(guild_id)
        )

    async def get_afk_status(self, guild_id, user_id):
        """
        Returns user's AFK status reason if set, None otherwise.
        """

        status = await self.sql.get_afk_status(guild_id, user_id)

        if status == None:
            return None
        
        return status

    async def clear_afk_status(self, guild_id, user_id):
        """
        Clears the AFK status of the user.
        """
        
        await self.sql.remove_afk_status(guild_id, user_id)

    async def set_afk_status(self, guild_id, user_id, reason):
        """
        Sets the AFK status of the user.
        """

        await self.sql.set_afk_status(guild_id, user_id, reason)

    #Birthday related
    async def set_birthday_channels(self, guild_id, calendar_channel, greet_channel):
        """
        Sets the channels to use for birthday stuff.
        """
        await self.sql.set_birthday_channels(guild_id, calendar_channel, greet_channel)

    async def get_birthday_channels(self, guild_id):
        """
        Returns the tuple of channels to be used for birthday stuff.
        Returns None if entry does not exists.
        """
        return await self.sql.get_birthday_channels(guild_id)

    async def get_birthday_kids(self):
        """
        Returns a map of user ids which have their birthday today.
        Returns n
        """

        date = datetime.datetime.utcnow()
        return await self.sql.get_birthday_kids(date.month, date.day)

    async def set_birthdate(self, user_id, month, day):
        """
        Updates your birthdate. 
        """
        await self.sql.set_user_birthdate(user_id, month, day)

    async def has_greeted_today(self):
        """
        Returns true if bot has completed greetings for today.
        """
        date = datetime.datetime.utcnow()
        return await self.sql.get_birthday_completion_date() == (date.month, date.day)

    async def update_greet_completion_date(self):
        """
        Updates the completion date in SQL, declaring that we have
        greeted all the birthdays today
        """

        date = datetime.datetime.utcnow()
        await self.sql.update_bithday_completion_date(date.month, date.day)