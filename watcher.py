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

    def on_any_event(self, event):
        """Called on any filesystem event."""
        self._changed.set()
        if self.callback:
            self.callback()

    def has_changed(self) -> bool:
        """Check if changes have been detected."""
        return self._changed.is_set()

    def clear(self):
        """Clear the changed flag."""
        self._changed.clear()


class GitWatcher:
    """Watches a git repository for changes."""

    def __init__(self, repo_path: Path, callback=None):
        self.repo_path = Path(repo_path).resolve()
        self.callback = callback
        self.observer: Observer | None = None
        self.handler: GitChangeHandler | None = None
        self._running = False

    def start(self):
        """Start watching the repository."""
        if self._running:
            return
        self.handler = GitChangeHandler(callback=self.callback)
        self.observer = Observer()
        self.observer.schedule(self.handler, str(self.repo_path), recursive=True)
        self.observer.start()
        self._running = True

    def stop(self):
        """Stop watching the repository."""
        if not self._running:
            return
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=1.0)
            self.observer = None
        self._running = False
