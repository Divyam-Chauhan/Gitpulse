"""Configuration settings for GitPulse dashboard."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Dashboard configuration."""
    refresh_rate: float = 2.0
    repo_path: Path = None

    colors = {
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
