from database import Database
from bookmark import BookmarkFolder

with Database('./bookmark-box.sqlite') as db:
    # create a new bookmark folder and save it to the database
    folder = BookmarkFolder(icon='😎', title='test', links={'Google': 'https://www.google.com', 'Facebook': 'https://www.facebook.com'})
    folder.save_to_db(db.conn)

    # load the bookmark folder from the database
    folder = BookmarkFolder.load_from_db(db.conn, 'test')
    print(folder)

    # list all bookmark folders in the database
    folder_titles = BookmarkFolder.list_all_folders(db.conn)
    print(folder_titles)

    