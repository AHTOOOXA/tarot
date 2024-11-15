import os
from pathlib import Path


class FileManager:
    def __init__(self):
        # Get the absolute path to the src directory
        self.src_path = Path(__file__).parent.parent
        self.static_path = self.src_path / "static"
        self.images_path = self.static_path / "images"

        # Create directories if they don't exist
        self.static_path.mkdir(exist_ok=True)
        self.images_path.mkdir(exist_ok=True)

    def get_image_path(self, image_name: str) -> Path:
        """Get absolute path to image in static/images directory"""
        return self.images_path / image_name

    def ensure_image_exists(self, image_name: str) -> bool:
        """Check if image exists in static/images directory"""
        return (self.images_path / image_name).exists()


# Create singleton instance
file_manager = FileManager()
