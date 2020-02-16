from .. import repository
from .. import constants

#Import required fixtures here
from . import fixtures
fix_delete_db = fixtures.delete_db

GUILD_ID = 552466467
GUILD2_ID = 77551166

def test():
    repo = repository.Repository('_test.db')

    assert repo.get_prefix(GUILD_ID) == constants.DEFAULT_COMMAND_PREFIX

    repo.set_prefix(GUILD_ID, '$')
    repo.set_prefix(GUILD2_ID, '#')

    assert repo.get_prefix(GUILD2_ID) == '#'
    assert repo.get_prefix(GUILD_ID) == '$'