import pytest

from .. import repository

#Fixtures
from . import fixtures
fix_delete_db = fixtures.delete_db

GUILD1 = 55
GUILD2 = 66
ROLE1 = 5
ROLE2 = 3

@pytest.mark.asyncio()
async def test_add_remove():
    repo = repository.Repository('_test.db')

    assert await repo.add_mod_role(GUILD1, ROLE1)
    assert await repo.add_mod_role(GUILD2, ROLE1)

    assert await repo.delete_mod_role(GUILD1, ROLE1)

    assert not await repo.delete_mod_role(GUILD1, ROLE1)
    assert not await repo.delete_mod_role(GUILD1, ROLE2)
    assert not await repo.delete_mod_role(GUILD2, ROLE2)

    assert await repo.delete_mod_role(GUILD2, ROLE1)

    #These two stay in db
    assert await repo.add_mod_role(GUILD1, ROLE2)
    assert await repo.add_mod_role(GUILD2, ROLE2)