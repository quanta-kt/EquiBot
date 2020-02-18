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