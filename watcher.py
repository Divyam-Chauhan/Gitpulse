"""Filesystem watcher for git repository changes using watchdog."""
import threading
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class GitChangeHandler(FileSystemEventHandler):
    """Handles filesystem events in the git repository."""

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self._changed = threading.Event()


class GitWatcher:
    """Watches a git repository for changes."""

    def __init__(self, repo_path: Path, callback=None):
        self.repo_path = Path(repo_path).resolve()
        self.callback = callback
        self.observer: Observer | None = None
        self.handler: GitChangeHandler | None = None
        self._running = False
