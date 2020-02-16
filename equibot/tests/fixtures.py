import pytest

@pytest.fixture(autouse=True)
def delete_db():
    import os
    if os.path.exists('_test.db'):
        os.remove('_test.db')