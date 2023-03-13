import sqlite3
import os
import pytest

from database import Database


# create a fixture to setup and teardown the test database and data
@pytest.fixture(scope='module')
def setup_teardown():
    # create a test database and connect to it
    test_db_name = 'test_bookmarks.sqlite'
    with Database(test_db_name) as db:
        # yield connection to tests
        yield db.conn
    os.remove(test_db_name)

# test case for checking that the bookmark_folder table is created in the database
def test_create_table(setup_teardown):
    cursor = setup_teardown.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookmark_folder'")
    assert cursor.fetchone() is not None

# test case for checking that a bookmark folder can be added to the database
def test_add_folder(setup_teardown):
    cursor = setup_teardown.cursor()

    # add a bookmark folder to the database
    cursor.execute("INSERT INTO bookmark_folder (title, icon, links) VALUES (?, ?, ?)", ('My Folder', 'https://example.com/icon.png', '{}'))
    setup_teardown.commit()

    # retrieve the bookmark folder from the database and check that it matches the added folder
    cursor.execute("SELECT * FROM bookmark_folder WHERE title=?", ('My Folder',))
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == 'My Folder'
    assert result[1] == 'https://example.com/icon.png'
    assert result[2] == '{}'
