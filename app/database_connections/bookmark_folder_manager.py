import sqlite3
from typing import Dict, List
import json

class BookmarkFolder:
    """
    Represents a folder of bookmarks with an icon, a title, and a dictionary of links.

    Attributes:
        icon (str): The icon for the bookmark.
        title (str): The title of the bookmark.
        links (dict): A dictionary of links.
    """

    def __init__(self, icon: str, title: str, links: Dict[str, str]) -> None:
        """
        Creates a new BookmarkFolder object with the given icon, title, and links.
        """
        self.icon = icon
        self.title = title
        self.links = links

    def to_dict(self) -> Dict[str, any]:
        """
        Returns a dictionary representation of the bookmark folder.
        """
        return {
            'icon': self.icon,
            'title': self.title,
            'links': self.links
        }

    @classmethod
    def from_dict(cls, bookmark_dict: Dict[str, any]) -> 'BookmarkFolder':
        """
        Creates a new BookmarkFolder object from a dictionary.
        """
        return cls(
            icon=bookmark_dict['icon'],
            title=bookmark_dict['title'],
            links=bookmark_dict['links']
        )

    def to_json(self) -> str:
        """
        Returns a JSON string representation of the bookmark folder.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'BookmarkFolder':
        """
        Creates a new Bookmark object from a JSON string.
        """
        return cls.from_dict(json.loads(json_str))
    
    def add_link(self, name: str, url: str) -> None:
        """
        Adds a new link to the bookmark folder.
        """
        self.links[name] = url

    def __str__(self) -> str:
        """
        Returns a string representation of the bookmark folder.
        """
        return f"BookmarkFolder(icon={self.icon}, title={self.title}, links={self.links})"

    def save_to_db(self, conn: sqlite3.Connection) -> None:
        """
        Saves the bookmark folder to the database.
        """
        conn.execute("INSERT OR REPLACE INTO bookmark_folder (title, icon, links) VALUES (?, ?, ?)", (self.title, self.icon, json.dumps(self.links)))
        conn.commit()

    @classmethod
    def load_from_db(cls, conn: sqlite3.Connection, title: str) -> 'BookmarkFolder':
        """
        Loads a bookmark folder from the database.
        """
        result = conn.execute("SELECT * FROM bookmark_folder WHERE title=?", (title,)).fetchone()
        if result is None:
            raise ValueError(f"Bookmark folder with title '{title}' does not exist in database.")
        return cls(
            icon=result[1],
            title=result[0],
            links=json.loads(result[2])
        )

    @classmethod
    def list_all_folders(cls, conn: sqlite3.Connection) -> List[str]:
        """
        Returns a list of titles of all bookmark folders in the database.
        """
        result = conn.execute("SELECT title FROM bookmark_folder").fetchall()
        return [row[0] for row in result]