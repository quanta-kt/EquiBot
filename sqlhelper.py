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

def connect_db():
    try:
        conn = sqlite3.connect('database.sql')
        if conn != None:
            print("Connected to database")
            return conn
        else:
            sys.stderr.write("Cannot create database connection. ;-;")
    except sqlite3.Error as error:
        sys.stderr.write(error)

def init_prefix_table():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_create_prefix_table)
    except sqlite3.Error as e:
        sys.stderr.write(e)
    finally:
        if conn:
            conn.close()


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
        sys.stderr.write(e)
    finally:
        if conn:
            conn.close()

def update_guild_prefix(guild_id, new_prefix):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_update_prefix_for_guild, (guild_id, new_prefix))
        conn.commit()
    except sqlite3.Error as e:
        sys.stderr.write(e)
    finally:
        if conn:
            conn.close()
