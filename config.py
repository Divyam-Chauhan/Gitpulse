"""Configuration settings for GitPulse dashboard."""
import os
from dataclasses import dataclass
from pathlib import Path


# Color scheme for the dashboard
COLORS = {
    "primary": "cyan",
    "secondary": "blue",
    "accent": "bright_yellow",
    "success": "green",
    "warning": "yellow",
    "error": "red",
    "muted": "dim",
    "branch": "bright_cyan",
    "commit_hash": "bright_yellow",
    "author": "bright_green",
    "time": "dim",
    "staged": "green",
    "unstaged": "yellow",
    "untracked": "red",
    "header": "bright_blue",
    "border": "blue",
    "footer": "dim",
}

# Panel title style
PANEL_TITLE_STYLE = "bold bright_white"

VERSION = "1.0.0"

@dataclass
class Config:
    """Dashboard configuration."""
    refresh_rate: float = 2.0
    repo_path: Path = None

    def __post_init__(self):
        if self.repo_path is None:
            self.repo_path = self._find_git_root()

    def _find_git_root(self) -> Path:
        """Find git repository root from current directory."""
        cwd = Path(os.getcwd()).resolve()
        current = cwd
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent
        return cwd

    @property
    def is_git_repo(self) -> bool:
        """Check if configured path is a valid git repository."""
        return (self.repo_path / ".git").is_dir()
