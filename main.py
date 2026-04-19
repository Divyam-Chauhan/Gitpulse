"""GitPulse - Real-time Terminal Git Dashboard."""
import argparse
import sys
import time
from pathlib import Path
from datetime import datetime

from rich.live import Live

from config import Config, VERSION
import subprocess
from ui import Dashboard, GitData
from watcher import GitWatcher


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="GitPulse - Real-time Terminal Git Dashboard"
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="Path to git repository (default: auto-detect)"
    )
    parser.add_argument(
        "--refresh",
        type=float,
        default=2.0,
        help="Refresh rate in seconds (default: 2.0)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"GitPulse {VERSION}"
    )
    return parser.parse_args()


def build_git_data(git_parser, repo_path: Path) -> GitData:
    """Build GitData from current repository state."""
    return GitData(
        branch=git_parser.get_current_branch(),
        last_commit=git_parser.get_last_commit(),
        status=git_parser.get_status_counts(),
        recent_commits=git_parser.get_recent_commits(),
        today_changes=git_parser.get_today_changes(),
        repo_path=str(repo_path),
        refresh_time=datetime.now().strftime("%H:%M:%S")
    )


def main():
    """Main entry point for GitPulse dashboard."""
    # Check if git is installed
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
    except FileNotFoundError:
        print("Error: git is not installed or not found in PATH.")
        sys.exit(1)

    from git_parser import GitParser
    
    args = parse_args()
    config = Config(refresh_rate=args.refresh, repo_path=args.path)

    if not config.is_git_repo:
        print(f"Error: {config.repo_path} is not a valid git repository")
        sys.exit(1)

    print(f"Starting GitPulse for: {config.repo_path}")
    print(f"Refresh rate: {config.refresh_rate}s")
    print("Press Ctrl+C to exit\n")
    time.sleep(1)

    dashboard = Dashboard()
    git_parser = GitParser(config.repo_path)
    watcher = GitWatcher(config.repo_path)

    # Setup: Initialize watcher
    watcher.start()

    try:
        # Initial data load
        data = build_git_data(git_parser, config.repo_path)
        dashboard.update(data)

        with Live(
            dashboard.layout,
            console=dashboard.console,
            refresh_per_second=1,
            screen=True
        ) as live:
            while True:
                # Check for file changes, but also refresh periodically
                has_file_change = watcher.has_changes()
                if has_file_change:
                    watcher.clear_changes()

                data = build_git_data(git_parser, config.repo_path)
                dashboard.update(data)
                time.sleep(config.refresh_rate)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        watcher.stop()


if __name__ == "__main__":
    main()
