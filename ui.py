"""Rich UI components for the GitPulse dashboard."""
from dataclasses import dataclass


@dataclass
class GitData:
    """Container for all git data to display."""
    branch: str = "N/A"
    last_commit: dict = None
    status: dict = None
    recent_commits: list = None
    today_changes: list = None
    repo_path: str = ""
    refresh_time: str = ""

    def __post_init__(self):
        if self.last_commit is None:
            self.last_commit = {"hash": "", "message": "", "author": "", "time": ""}
        if self.status is None:
            self.status = {"staged": 0, "unstaged": 0, "untracked": 0}
        if self.recent_commits is None:
            self.recent_commits = []
        if self.today_changes is None:
            self.today_changes = []
