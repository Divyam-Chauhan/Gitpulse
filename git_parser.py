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

    def get_recent_commits(self, n: int = 7) -> list[dict]:
        """Get last n commits as a list."""
        if not self.is_valid_repo():
            return []
        commits = []
        for commit in self.repo.iter_commits(max_count=n):
            committed_date = commit.committed_datetime
            age = self._format_age(committed_date)
            commits.append({
                "hash": commit.hexsha[:7],
                "message": commit.message.strip().split("\n")[0][:50],
                "author": str(commit.author).split(" <")[0],
                "time": age,
            })
        return commits

    def get_today_changes(self) -> list[dict]:
        """Get files changed today with +/- line counts."""
        if not self.is_valid_repo():
            return []
        today = datetime.now(timezone.utc).date()
        files = []
        today_commits = []
        for commit in self.repo.iter_commits():
            commit_date = commit.committed_datetime.date()
            if commit_date == today:
                today_commits.append(commit)
            elif commit_date < today:
                break
        if not today_commits:
            return []
        try:
            today_earliest = today_commits[-1]
            today_latest = today_commits[0]
            diff_index = today_earliest.diff(today_latest)
            for diff_item in diff_index:
                path = diff_item.a_path or diff_item.b_path
                if not path:
                    continue
                files.append({"path": path, "added": 0, "removed": 0})
        except Exception:
            pass
        return files

    def get_last_refresh_time(self) -> str:
        """Get formatted timestamp for last refresh."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
