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
        content = Text(f"Branch: {self.data.branch}")
        return Panel(content, title="Repository", border_style=COLORS["primary"])

    def _render_top_right(self) -> Panel:
        """Render last commit info."""
        content = Text("Last commit info pending...")
        return Panel(content, title="Latest Commit", border_style=COLORS["secondary"])

    def _render_bottom_left(self) -> Table:
        """Render recent commits table."""
        table = Table(title="Recent Commits", box=box.SIMPLE)
        table.add_column("Hash", style=COLORS["accent"])
        table.add_column("Message")
        return table

    def _render_bottom_right(self) -> Panel:
        """Render today's changes panel."""
        content = Text("Today's changes pending...")
        return Panel(content, title="Today's Changes", border_style=COLORS["success"])

    def _render_footer(self) -> Panel:
        """Render footer with status info."""
        content = Text(f"GitPulse | {self.data.repo_path} | Last refresh: {self.data.refresh_time}")
        return Panel(content, style=PANEL_TITLE_STYLE)
