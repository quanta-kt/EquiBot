import sqlite3
import sys
import constants

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

def connect_db():
    try:
        conn = sqlite3.connect('database.sql')
        if conn != None:
            return conn
        else:
            raise sqlite3.Error("Can not connect to database!")
    except sqlite3.Error as e:
        print(e, file=sys.stderr)

def create_tables():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_create_prefix_table)
        cursor.execute(sql_create_modrole_table)
    except sqlite3.Error as e:
        print(e, file=sys.stderr)
    finally:
        if conn: conn.close()


def get_guild_prefix(guild_id):
    try:
        conn = connect_db()
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

def update_guild_prefix(guild_id, new_prefix):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_update_prefix_for_guild, (guild_id, new_prefix))
        conn.commit()
    except sqlite3.Error as e:
        print(e, file=sys.stderr)
    finally:
        if conn: conn.close()

def add_moderator_role(guild_id, role_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_insert_modrole, (guild_id, role_id))
        conn.commit()
    except sqlite3.Error as e:
        print(e, file=sys.stderr)
    finally:
        if conn: conn.close()

def delete_moderator_role(entry_key):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_delete_modrole, (entry_key,))
        conn.commit()
    except sqlite3.Error as e:
        print(e, file=sys.stderr)
    finally:
        if conn: conn.close()

def get_moderator_roles(guild_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_get_modroles, (guild_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e, file=sys.stderr)
    finally:
        if conn: conn.close()

#Index refers to the PRIMARY KEY column of the table
def get_moderator_roles_with_index(guild_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_get_modroles_and_index, (guild_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e, file=sys.stderr)
    finally:
        if conn: conn.close
