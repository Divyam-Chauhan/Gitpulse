"""Git repository data parser using subprocess and gitpython."""
from datetime import datetime, timezone
from pathlib import Path

from git import Repo
from git.exc import InvalidGitRepositoryError


class GitParser:
    """Parses git repository information."""

    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)
        try:
            self.repo = Repo(self.repo_path)
        except InvalidGitRepositoryError:
            self.repo = None

    def is_valid_repo(self) -> bool:
        """Check if this is a valid git repository."""
        return self.repo is not None and not self.repo.bare

    def get_current_branch(self) -> str:
        """Get current branch name or detached HEAD state."""
        if not self.is_valid_repo():
            return "N/A"
        try:
            return self.repo.active_branch.name
        except Exception:
            head = self.repo.head.commit
            return f"detached ({head.hexsha[:7]})"

    def _format_age(self, dt: datetime) -> str:
        """Format a datetime as relative age string."""
        now = datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = now - dt
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return f"{seconds}s ago"
        elif seconds < 3600:
            return f"{seconds // 60}m ago"
        elif seconds < 86400:
            return f"{seconds // 3600}h ago"
        elif seconds < 604800:
            return f"{seconds // 86400}d ago"
        else:
            return f"{seconds // 604800}w ago"

    def get_last_commit(self) -> dict:
        """Get info about the most recent commit."""
        if not self.is_valid_repo():
            return {"hash": "", "message": "", "author": "", "time": ""}
        commit = self.repo.head.commit
        committed_date = commit.committed_datetime
        age = self._format_age(committed_date)
        return {
            "hash": commit.hexsha[:7],
            "message": commit.message.strip().split("\n")[0],
            "author": str(commit.author),
            "time": age,
        }

    def get_status_counts(self) -> dict[str, int]:
        """Get counts of staged, unstaged, and untracked files."""
        if not self.is_valid_repo():
            return {"staged": 0, "unstaged": 0, "untracked": 0}
        staged = len(self.repo.index.diff("HEAD"))
        unstaged = len(self.repo.index.diff(None))
        untracked = len(self.repo.untracked_files)
        return {"staged": staged, "unstaged": unstaged, "untracked": untracked}
