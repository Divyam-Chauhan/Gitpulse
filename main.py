"""GitPulse - Real-time Terminal Git Dashboard."""
import argparse
import sys
from pathlib import Path

from config import Config
from git_parser import GitParser
from ui import Dashboard, GitData
from watcher import RepoWatcher


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
    return parser.parse_args()


def main():
    """Main entry point for GitPulse dashboard."""
    args = parse_args()
    config = Config(refresh_rate=args.refresh, repo_path=args.path)

    if not config.is_git_repo:
        print(f"Error: {config.repo_path} is not a valid git repository")
        sys.exit(1)

    dashboard = Dashboard()
    git_parser = GitParser(config.repo_path)
    watcher = RepoWatcher(config.repo_path)

    # TODO: Implement setup phase
    # TODO: Implement live loop
    # TODO: Implement teardown


if __name__ == "__main__":
    main()
