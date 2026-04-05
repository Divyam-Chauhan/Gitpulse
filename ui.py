"""Rich UI components for the GitPulse dashboard."""
from dataclasses import dataclass

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from config import COLORS, PANEL_TITLE_STYLE


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


class Dashboard:
    """Main dashboard layout for GitPulse."""

    def __init__(self):
        self.console = Console()
        self.layout = Layout()

        # Configure the main layout
        self.layout.split_column(
            Layout(name="main", ratio=4),
            Layout(name="footer", size=3)
        )

        # Split main area into top and bottom rows
        self.layout["main"].split_row(
            Layout(name="top"),
            Layout(name="bottom")
        )

        # Split top row into two panels
        self.layout["top"].split_row(
            Layout(name="top_left"),
            Layout(name="top_right")
        )

        # Split bottom row into two panels
        self.layout["bottom"].split_row(
            Layout(name="bottom_left"),
            Layout(name="bottom_right")
        )

    def update(self, data: GitData):
        """Update all panels with new git data."""
        self.data = data
        self.layout["top_left"].update(self._render_top_left())
        self.layout["top_right"].update(self._render_top_right())
        self.layout["bottom_left"].update(self._render_bottom_left())
        self.layout["bottom_right"].update(self._render_bottom_right())
        self.layout["footer"].update(self._render_footer())

    def _render_top_left(self) -> Panel:
        """Render branch and status info."""
        status = self.data.status

        # Build status lines with color coding
        status_text = Text()
        status_text.append("Branch: ", style="bold")
        status_text.append(self.data.branch, style=COLORS["accent"])
        status_text.append("\n\n")

        status_text.append("● ", style=COLORS["success"])
        status_text.append(f"Staged: {status.get('staged', 0)}\n")
        status_text.append("● ", style=COLORS["warning"])
        status_text.append(f"Unstaged: {status.get('unstaged', 0)}\n")
        status_text.append("● ", style=COLORS["muted"])
        status_text.append(f"Untracked: {status.get('untracked', 0)}")

        return Panel(
            status_text,
            title=Text("Repository Status", style=PANEL_TITLE_STYLE),
            border_style=COLORS["primary"],
            padding=(1, 2)
        )

    def _render_top_right(self) -> Panel:
        """Render last commit info."""
        commit = self.data.last_commit

        commit_text = Text()
        commit_text.append("Hash: ", style="bold")
        commit_text.append(commit.get("hash", "N/A")[:7], style=COLORS["accent"])
        commit_text.append("\n\n")

        commit_text.append("Message: ", style="bold")
        commit_text.append(commit.get("message", "N/A"))
        commit_text.append("\n\n")

        commit_text.append("Author: ", style="bold")
        commit_text.append(commit.get("author", "N/A"))
        commit_text.append("\n")

        commit_text.append("Time: ", style="bold")
        commit_text.append(commit.get("time", "N/A"), style=COLORS["muted"])

        return Panel(
            commit_text,
            title=Text("Latest Commit", style=PANEL_TITLE_STYLE),
            border_style=COLORS["secondary"],
            padding=(1, 2)
        )

    def _render_bottom_left(self) -> Panel:
        """Render recent commits table."""
        table = Table(
            box=box.SIMPLE,
            show_header=True,
            header_style="bold",
            expand=True,
            row_styles=["", "dim"]
        )
        table.add_column("Hash", style=COLORS["accent"], width=8, no_wrap=True)
        table.add_column("Message", ratio=2, overflow="ellipsis")
        table.add_column("Author", style=COLORS["secondary"], width=15, no_wrap=True)
        table.add_column("Time", style=COLORS["muted"], width=12, no_wrap=True)

        for commit in self.data.recent_commits[:10]:
            msg = commit.get("message", "")
            if len(msg) > 50:
                msg = msg[:47] + "..."
            table.add_row(
                commit.get("hash", "N/A")[:7],
                msg,
                commit.get("author", "N/A")[:14],
                commit.get("time", "N/A")
            )

        return Panel(
            table,
            title=Text("Recent Commits", style=PANEL_TITLE_STYLE),
            border_style=COLORS["accent"],
            padding=(1, 1)
        )

    def _render_bottom_right(self) -> Panel:
        """Render today's changes panel."""
        content = Text("Today's changes pending...")
        return Panel(content, title="Today's Changes", border_style=COLORS["success"])

    def _render_footer(self) -> Panel:
        """Render footer with status info."""
        content = Text(f"GitPulse | {self.data.repo_path} | Last refresh: {self.data.refresh_time}")
        return Panel(content, style=PANEL_TITLE_STYLE)
