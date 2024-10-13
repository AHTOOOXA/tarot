import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sys


class RestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_bot()

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected change in {event.src_path}. Restarting bot...")
            self.restart_bot()

    def start_bot(self):
        self.process = subprocess.Popen([sys.executable, "-m", "app.tgbot.bot"])

    def restart_bot(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.start_bot()


if __name__ == "__main__":
    path = "."
    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
