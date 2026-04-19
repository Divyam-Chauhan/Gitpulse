# Changelog

All notable changes to GitPulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.0] - 2026-04-06

### Added

- Live auto-refreshing terminal dashboard using Rich
- Repository Status panel — current branch, staged, unstaged, and untracked file counts
- Latest Commit panel — hash, message, author, and relative timestamp
- Recent Commits table — last 7 commits with hash, message, author, and time
- Today's Changes panel — files modified today with `+/-` line diff statistics
- Filesystem watcher via `watchdog` for instant updates on file changes
- CLI `--path` flag to monitor an external git repository
- CLI `--refresh` flag to customize the refresh interval (default: 2.0s)
- Graceful exit on `Ctrl+C`
- Auto-detection of git repository root from current working directory
