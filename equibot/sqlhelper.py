import sqlite3
import sys

from . import constants

sql_create_prefix_table = """
    CREATE TABLE IF NOT EXISTS prefixes(
        guild_id INTEGER PRIMARY KEY,
        prefix TEXT
    );"""

sql_get_prefix_for_guild = """
    SELECT prefix FROM prefixes
    WHERE guild_id = ?"""

sql_update_prefix_for_guild = """
    INSERT OR REPLACE INTO prefixes(guild_id, prefix)
    VALUES (?, ?)"""

sql_create_modrole_table = """
    CREATE TABLE IF NOT EXISTS modroles (
        id INTEGER PRIMARY KEY,
        guild_id INTEGER,
        role_id INTEGER
    );"""

sql_get_modroles = """
    SELECT role_id
    FROM modroles
    WHERE guild_id = ?"""

#Note: 'index' refers to table's PRIMARY KEY
sql_get_modroles_and_index = """ 
    SELECT id, role_id
    FROM modroles
    WHERE guild_id = ?"""

sql_insert_modrole = """
    INSERT INTO modroles(guild_id, role_id)
    VALUES (?, ?)"""

sql_delete_modrole = """
    DELETE FROM modroles
    WHERE id = ?"""

sql_create_afk_table = """
    CREATE TABLE IF NOT EXISTS afk_table(
        id INTEGER PRIMARY KEY,
        guild_id INTEGER,
        user_id INTEGER,
        reason TEXT
    )"""

sql_set_afk = """
    INSERT INTO afk_table(guild_id, user_id, reason)
    VALUES(?, ?, ?)"""

sql_remove_afk = """
    DELETE FROM afk_table
    WHERE guild_id = ? AND user_id = ?"""

sql_get_user_afk_status = """
    SELECT reason from afk_table
    WHERE guild_id = ? AND user_id = ?"""

#Birthday related
sql_create_bithday_channels_table = """
    CREATE TABLE IF NOT EXISTS birthday_channels(
        guild_id INTEGER PRIMARY KEY,
        calendar_channel_id INTEGER NOT NULL,
        greet_channel_id INTEGER NOT NULL
    )"""

sql_set_birthday_channels = """
    INSERT INTO birthday_channels(guild_id, calendar_channel_id, greet_channel_id)
    VALUES(?, ?, ?)
    ON CONFLICT(guild_id) 
    DO UPDATE SET
        calendar_channel_id=excluded.calendar_channel_id,
        greet_channel_id=excluded.greet_channel_id
    """

sql_get_bithday_channels = """
    SELECT calendar_channel_id, greet_channel_id
    FROM birthday_channels
    WHERE guild_id = ?
    """

sql_create_birthdate_table = """
    CREATE TABLE IF NOT EXISTS birthdates(
        user_id INTEGER PRIMARY KEY,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL
    )"""

sql_set_birthdate = """
    INSERT INTO birthdates(user_id, month, day)
    VALUES(?, ?, ?)
    ON CONFLICT(user_id)
    DO UPDATE SET
        month=excluded.month,
        day=excluded.day
    """

sql_get_birthdate = """
    SELECT month, day
    FROM birthdates
    WHERE user_id = ?
    """

sql_get_birthday_kids = """
    SELECT user_id FROM birthdates
    WHERE month = ? AND day = ?
    """

#Table holds only a single row
#It is the date of last completion of birthday greets
#If it is the same as today's date, we should skip greeting (as it would be already done)
sql_create_birthday_completion_table = """
    CREATE TABLE IF NOT EXISTS birthday_completion(
        id INTEGER PRIMARY KEY,
        month INTEGER,
        day INTEGER
    )
    """

sql_create_birthday_completion_row = """
    INSERT OR IGNORE INTO birthday_completion(id, month, day)
    VALUES(0, 0, 0)
    """

sql_update_birthday_completion_date = """
    UPDATE birthday_completion
    SET month = ?, day = ?
    WHERE id = 0
    """

sql_get_bithday_completion_date = """
    SELECT month, day
    FROM birthday_completion
    WHERE id = 0
    """

#Message IDs for calendar messages.
sql_create_calendar_messages_table = """
    CREATE TABLE IF NOT EXISTS calendar_messages(
        guild_id    INTEGER PRIMARY KEY,
        january     INTEGER NOT NULL,
        february    INTEGER NOT NULL,
        march       INTEGER NOT NULL,
        april       INTEGER NOT NULL,
        may         INTEGER NOT NULL,
        june        INTEGER NOT NULL,
        july        INTEGER NOT NULL,
        august      INTEGER NOT NULL,
        september   INTEGER NOT NULL,
        october     INTEGER NOT NULL,
        november    INTEGER NOT NULL,
        december    INTEGER NOT NULL
    )
    """

sql_update_calendar_message_ids = """
    INSERT INTO calendar_messages(
        guild_id, january, february, march,
        april, may, june, july, august,
        september, october, november, december
    )
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    ON CONFLICT(guild_id)
    DO UPDATE SET
        january   =  excluded.january  ,
        february  =  excluded.february ,
        march     =  excluded.march    ,
        april     =  excluded.april    ,
        may       =  excluded.may      ,
        june      =  excluded.june     ,
        july      =  excluded.july     ,
        august    =  excluded.august   ,
        september =  excluded.september,
        october   =  excluded.october  ,
        november  =  excluded.november ,
        december  =  excluded.december 
    """

sql_clear_calendar_message_ids = """
    DELETE FROM calendar_messages
    WHERE guild_id = ?
    """

sql_get_calendar_messages = """
    SELECT january, february, march,
        april, may, june, july, august,
        september, october, november, december

    FROM calendar_messages
    WHERE guild_id = ?
    """

sql_create_birthday_ping_role_table = """
    CREATE TABLE IF NOT EXISTS birthday_ping(
        guild_id INTEGER PRIMARY KEY,
        role_id INTEGER
    )
    """

sql_set_birthday_ping_role = """
    INSERT INTO birthday_ping(guild_id, role_id)
    VALUES(?, ?)

    ON CONFLICT(guild_id)
    DO UPDATE SET role_id = excluded.role_id
    """

sql_get_birthday_ping_role = """
    SELECT role_id
    FROM birthday_ping
    WHERE guild_id = ?"""

class SqlHelper:
    """
    Class used for running SQL queries.
    Not to be used directly, use `Repository` class for reading/writing data.
    """

    @classmethod
    async def create(cls, filename):
        sql = SqlHelper()
        sql.db_file = filename
        await sql.create_tables()
        return sql

    def connect_db(self):
        try:
            conn = sqlite3.connect(self.db_file)
            if conn != None:
                return conn
            else:
                raise sqlite3.Error("Can not connect to database!")
        except sqlite3.Error as e:
            print(e, file=sys.stderr)

    async def create_tables(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_create_prefix_table)
            cursor.execute(sql_create_modrole_table)
            cursor.execute(sql_create_afk_table)
            cursor.execute(sql_create_bithday_channels_table)
            cursor.execute(sql_create_birthdate_table)
            cursor.execute(sql_create_birthday_completion_table)
            cursor.execute(sql_create_birthday_completion_row)
            conn.commit()
            cursor.execute(sql_create_calendar_messages_table)
            cursor.execute(sql_create_birthday_ping_role_table)
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()


    def get_guild_prefix(self, guild_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_prefix_for_guild, (guild_id,))
            result = cursor.fetchone()

            if result is None:
                return None
            else:
                return result[0]

        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def update_guild_prefix(self, guild_id, new_prefix):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_update_prefix_for_guild, (guild_id, new_prefix))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def add_moderator_role(self, guild_id, role_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_insert_modrole, (guild_id, role_id))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def delete_moderator_role(self, entry_key):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_delete_modrole, (entry_key,))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def get_moderator_roles(self, guild_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_modroles, (guild_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    #Index refers to the PRIMARY KEY column of the table
    async def get_moderator_roles_with_index(self, guild_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_modroles_and_index, (guild_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def set_afk_status(self, guild_id, user_id, reason):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_set_afk, (guild_id, user_id, reason))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def get_afk_status(self, guild_id, user_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_user_afk_status, (guild_id, user_id))
            result = cursor.fetchone()

            if result == None:
                return None
            else:
                return result[0]

        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def remove_afk_status(self, guild_id, user_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_remove_afk, (guild_id, user_id))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def set_birthday_channels(self, guild_id, calendar_channel, greet_channel):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_set_birthday_channels, (guild_id, calendar_channel, greet_channel))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def get_birthday_channels(self, guild_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_bithday_channels, (guild_id,))
            result = cursor.fetchone()

            if result == None:
                return None
            else:
                return result

        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def get_user_birthdate(self, user_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_birthdate, (user_id,))
            result = cursor.fetchone()

            if result == None:
                return None
            else:
                return result
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def set_user_birthdate(self, user_id, month, day):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_set_birthdate, (user_id, month, day))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def get_birthday_kids(self, month, day):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_birthday_kids, (month, day))
            result = cursor.fetchall()

            if result == None or len(result) == 0:
                return None
            else:
                return [x[0] for x in result]

        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def update_bithday_completion_date(self, month, day):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_update_birthday_completion_date, (month, day))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def get_birthday_completion_date(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_bithday_completion_date)

            return cursor.fetchone()

        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def update_calendar_message_ids(self, guild_id, ids):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_update_calendar_message_ids, (guild_id, *ids))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def clear_calendar_message_ids(self, guild_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_clear_calendar_message_ids, (guild_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def get_calendar_message_ids(self, guild_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_calendar_messages, (guild_id,))

            return cursor.fetchone()

        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def set_birthday_ping_role(self, guild_id, role_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_set_birthday_ping_role, (guild_id, role_id))
            conn.commit()
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()

    async def get_birthday_ping_role(self, guild_id):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(sql_get_birthday_ping_role, (guild_id,))

            if (result := cursor.fetchone()) != None:
                return result[0]

            return None

        except sqlite3.Error as e:
            print(e, file=sys.stderr)
        finally:
            if conn: conn.close()