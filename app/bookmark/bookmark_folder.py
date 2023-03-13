import sqlite3
from typing import Dict, List
import json
import emoji
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests

class BookmarkFolder:
    def __init__(self, icon: str, title: str, links: Dict[str, str]) -> None:
        self.title = title
        self.links = links
        if icon is None:
            # Render a favicon automatically if no icon is provided
            icon_filename = self.emoji_to_favicon()
            with open(icon_filename, "rb") as f:
                self.icon = f.read()
        else:
            self.icon = icon

    def add_link(self, name: str, url: str) -> None:
        self.links[name] = url

    def save_to_db(self, conn: sqlite3.Connection) -> None:
        # Convert the image data to a blob
        icon_blob = sqlite3.Binary(self.icon)

        # Save the bookmark folder to the database
        conn.execute(
            """
                INSERT OR REPLACE INTO bookmark_folder (
                    title, 
                    icon, 
                    links
                ) 
                VALUES (?, ?, ?)
            """,
            (
                self.title, 
                icon_blob, 
                json.dumps(self.links)
            )
        )
        conn.commit()

    @classmethod
    def load_from_db(cls, conn: sqlite3.Connection, title: str) -> 'BookmarkFolder':
        result = conn.execute("SELECT * FROM bookmark_folder WHERE title=?", (title,)).fetchone()
        if result is None:
            raise ValueError(f"Bookmark folder with title '{title}' does not exist in database.")

        # Convert the blob back to image data
        icon = result[1]

        return cls(
            icon=icon,
            title=result[0],
            links=json.loads(result[2])
        )


    def __str__(self) -> str:
        return f"BookmarkFolder(icon={self.icon}, title={self.title}, links={self.links})"

    @classmethod
    def list_all_folders(cls, conn: sqlite3.Connection) -> List[str]:
        result = conn.execute("SELECT title FROM bookmark_folder").fetchall()
        return [row[0] for row in result]

    @classmethod
    def favicon(text, font_size=16):
        # Set up image dimensions
        size = (16, 16)
        
        # Create an Image object
        im = Image.new('RGBA', size, (255, 255, 255, 0))
        
        # Create a Draw object
        draw = ImageDraw.Draw(im)
        
        # Set font and text size
        font = ImageFont.truetype("arial.ttf", font_size)
        
        # Get text dimensions
        text_width, text_height = draw.textsize(text, font=font)
        
        # Calculate position to center text
        x = (size[0] - text_width) / 2
        y = (size[1] - text_height) / 2
        
        # Draw text on image
        draw.text((x, y), text, font=font, fill=(0, 0, 0))
        
        # Save image as bytes to memory buffer
        buffer = BytesIO()
        im.save(buffer, format='PNG')
        
        return buffer.getvalue()

