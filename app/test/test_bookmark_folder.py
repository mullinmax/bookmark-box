import sqlite3
import pytest
import os

# from .database import Database
from bookmark import BookmarkFolder


# setup test data
test_folders = [
    BookmarkFolder(
        icon='https://example.com/icon.png', 
        title='My Bookmarks', 
        links={
            'Google': 'https://www.google.com', 
            'Facebook': 'https://www.facebook.com'
        }
    ),
    BookmarkFolder(
        icon='https://example.com/icon.png', 
        title='My Folder', 
        links={}
    ),
    BookmarkFolder(
        icon='https://example.com/icon.png', 
        title='Another Folder', 
        links={
            'GitHub': 'https://github.com'
        }
    )
]

# create a fixture to setup and teardown the test database and data
@pytest.fixture(scope='module')
def setup_teardown():

    # create a test database and connect to it
    test_db_name = 'test_bookmarks.sqlite'
    test_conn = sqlite3.connect(test_db_name)

    # create table
    test_conn.execute("CREATE TABLE IF NOT EXISTS bookmark_folder (title TEXT PRIMARY KEY, icon TEXT, links TEXT)")

    # add test data to table
    for folder in test_folders:
        test_conn.execute("INSERT INTO bookmark_folder (title, icon, links) VALUES (?, ?, ?)", (folder.title, folder.icon, folder.to_json()))
        test_conn.commit()

    # yield connection to tests
    yield test_conn

    # teardown - remove table and close connection
    test_conn.execute("DROP TABLE bookmark_folder")
    test_conn.close()

    # remove the test database file
    os.remove(test_db_name)

# test case for adding a link to a bookmark folder
def test_add_link(setup_teardown):
    # load bookmark folder from database
    folder = BookmarkFolder.load_from_db(setup_teardown, 'My Bookmarks')

    # add a new link to the folder
    folder.add_link('Reddit', 'https://www.reddit.com')
    assert 'Reddit' in folder.links
    assert folder.links['Reddit'] == 'https://www.reddit.com'

    # save the updated folder to the database
    folder.save_to_db(setup_teardown)

    # load the folder from the database again and verify that the link was added
    folder = BookmarkFolder.load_from_db(setup_teardown, 'My Bookmarks')
    assert 'Reddit' in folder.links
    assert folder.links['Reddit'] == 'https://www.reddit.com'

# test case for listing all bookmark folders in the database
def test_list_all_folders(setup_teardown):
    # get a list of all bookmark folders in the database
    folders = BookmarkFolder.list_all_folders(setup_teardown)
    assert len(folders) == len(test_folders)
    assert all(folder.title in folders for folder in test_folders)

# test case for loading a non-existent bookmark folder from the database
def test_load_nonexistent_folder(setup_teardown):
    with pytest.raises(ValueError):
        BookmarkFolder.load_from_db(setup_teardown, 'Nonexistent Folder')
