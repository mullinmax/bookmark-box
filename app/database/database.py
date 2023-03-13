import sqlite3

class Database:
    """
    A class for interacting with an SQLite database of bookmarks.
    """

    def __init__(self, db_name: str) -> None:
        """
        Creates a new Database object with the given name.
        """
        self.db_name = db_name

    def __enter__(self) -> 'Database':
        """
        Opens the database connection and returns the Database object.
        """
        self.conn = sqlite3.connect(self.db_name)
        setup_commands = [
            '''
                CREATE TABLE IF NOT EXISTS bookmark_folder
                (title TEXT PRIMARY KEY,
                icon TEXT,
                links TEXT)
            '''
        ]
        for command in setup_commands:
            self.conn.execute(command)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Closes the database connection.
        """
        self.conn.close()