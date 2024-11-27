import os
from pathlib import Path


class FileManager:
    def __init__(self):
        # Get the absolute path to the src directory
        self.src_path = Path(__file__).parent.parent
        self.static_path = self.src_path / "static"

        # Create directories if they don't exist
        self.static_path.mkdir(exist_ok=True)

    def get_full_path(self, file_name: str) -> Path:
        """Get absolute path to file in static directory"""
        return self.static_path / file_name


# Create singleton instance
file_manager = FileManager()
