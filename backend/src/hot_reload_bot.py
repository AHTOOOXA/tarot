import os
import subprocess
import sys
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class BotReloader(FileSystemEventHandler):
    def __init__(self, start_command):
        self.start_command = start_command
        self.bot_process = None
        self.start_bot()

    def start_bot(self):
        """Start the bot process."""
        if self.bot_process:
            print("Restarting bot...")
            self.bot_process.kill()
        print("Starting bot...")
        try:
            self.bot_process = subprocess.Popen(
                self.start_command,
                shell=False,
                stdout=sys.stdout,
                stderr=sys.stderr,
                universal_newlines=True,
                bufsize=1,
            )
        except Exception as e:
            print(f"Failed to start bot: {e}")

    def on_modified(self, event):
        """Restart the bot on .py file changes, excluding __pycache__ and .pyc files."""
        if event.is_directory or event.src_path.endswith((".pyc", "__pycache__")):
            return
        print(f"File change detected: {event.src_path}")
        self.start_bot()

    def stop_bot(self):
        """Stop the bot process gracefully."""
        if self.bot_process:
            print("Stopping bot...")
            self.bot_process.kill()
            self.bot_process.wait()


if __name__ == "__main__":
    # Add -u flag for unbuffered output
    bot_command = [sys.executable, "-u", "-m", "app.tgbot.bot"]

    # Initialize the bot reloader
    event_handler = BotReloader(bot_command)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)

    # Start watching for changes
    print("Watching for file changes...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down watcher...")
        observer.stop()

    observer.join()
    event_handler.stop_bot()
