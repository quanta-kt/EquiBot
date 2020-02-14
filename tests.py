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
import repository as repo
import os

#Remove the comment to delete the `database.sql` file automatically.
#This can be helpful for easing out the process.
#DO NOT commit to git with the comment removed.
# os.remove('database.sql')
sql.create_tables()

class TestPrefixCommand(unittest.TestCase):
    """
    Test cases for `prefix command`
    """

    def test_sql(self):
        """
        Tests the SQL functions of this command
        """

        GUILD_ID = 55

        self.assertEquals(repo.get_prefix(GUILD_ID), '~')

        sql.update_guild_prefix(55, "%")
        self.assertEquals(repo.get_prefix(GUILD_ID), '%')

class TestModRoleCommand(unittest.TestCase):
    """
    Test cases for `modrole` command
    """

    GUILD1 = 55
    GUILD2 = 66
    ROLE1 = 5
    ROLE2 = 3

    def test_add_remove(self):

        self.assertTrue(
            repo.add_mod_role(self.GUILD1, self.ROLE1)
        )

        self.assertTrue(
            repo.add_mod_role(self.GUILD2, self.ROLE1)
        )

        self.assertTrue(
            repo.delete_mod_role(self.GUILD1, self.ROLE1)
        )

        self.assertFalse(
            repo.delete_mod_role(self.GUILD1, self.ROLE2)
        )

        self.assertFalse(
            repo.delete_mod_role(self.GUILD2, self.ROLE2)
        )

        self.assertTrue(
            repo.delete_mod_role(self.GUILD2, self.ROLE1)
        )

if __name__ == '__main__':
    unittest.main()