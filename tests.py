#!/usr/bin/python3

"""
To be used for writting and running test.
Test assumes that the database is NOT created, therefore delete or rename the `database.sql` file
before running these.

Every bot command has it's own TestCase class. Other stuff can be tested in thier own
respective classes.
"""

import unittest
import repository as repo
import sqlhelper as sql
import os

#Remove the comment to delete the `database.sql` file automatically.
#This can be helpful for easing out the process.
#DO NOT commit to git with the comment removed.
# os.remove('database.sql')

class TestPrefixCommand(unittest.TestCase):
    """
    Test cases for `prefix command`
    """

    def test_sql(self):
        """
        Tests the SQL functions of this command
        """

        GUILD_ID = 55

        sql.init_prefix_table()

        self.assertEquals(repo.get_prefix(GUILD_ID), '~')

        sql.update_guild_prefix(55, "%")
        self.assertEquals(repo.get_prefix(GUILD_ID), '%')

if __name__ == '__main__':
    unittest.main()