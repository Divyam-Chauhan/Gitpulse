"""Git repository data parser using subprocess and gitpython."""
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
