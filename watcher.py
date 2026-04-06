"""Filesystem watcher for git repository changes using watchdog."""
import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class GitChangeHandler(FileSystemEventHandler):
    """Handles filesystem events in the git repository."""

    def __init__(self, callback=None, debounce_ms: float = 100.0):
        super().__init__()
        self.callback = callback
        self._changed = threading.Event()
        self._lock = threading.Lock()
        self._last_event_time = 0.0
        self._debounce_ms = debounce_ms / 1000.0

    def _should_process(self, event) -> bool:
        """Check if event should be processed, with debounce."""
        current_time = time.time()
        with self._lock:
            if current_time - self._last_event_time < self._debounce_ms:
                return False
            self._last_event_time = current_time
        return True

    def on_any_event(self, event):
        """Called on any filesystem event."""
        if ".git" in event.src_path:
            return
        if event.src_path.endswith("~") or ".swp" in event.src_path:
            return
        if not self._should_process(event):
            return
        with self._lock:
            self._changed.set()
        if self.callback:
            try:
                self.callback()
            except Exception:
                pass

    def has_changed(self) -> bool:
        """Check if changes have been detected."""
        with self._lock:
            return self._changed.is_set()

    def clear(self):
        """Clear the changed flag."""
        with self._lock:
            self._changed.clear()


class GitWatcher:
    """Watches a git repository for changes."""

    def __init__(self, repo_path: Path, callback=None):
        self.repo_path = Path(repo_path).resolve()
        self.callback = callback
        self.observer: Observer | None = None
        self.handler: GitChangeHandler | None = None
        self._running = False
        self._lock = threading.Lock()
        self._thread = None

    def start(self):
        """Start watching the repository."""
        with self._lock:
            if self._running:
                return
            self.handler = GitChangeHandler(callback=self.callback)
            self.observer = Observer()
            self.observer.schedule(self.handler, str(self.repo_path), recursive=True)
            self.observer.start()
            self._running = True

    def stop(self):
        """Stop watching the repository."""
        with self._lock:
            if not self._running:
                return
            if self.observer:
                self.observer.stop()
                self.observer = None
            self._running = False
        if self.observer:
            self.observer.join(timeout=1.0)

    def has_changes(self) -> bool:
        """Check if changes have been detected."""
        if self.handler:
            return self.handler.has_changed()
        return False

    def clear_changes(self):
        """Clear the changed flag."""
        if self.handler:
            self.handler.clear()
