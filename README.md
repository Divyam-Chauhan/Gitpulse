# GitPulse

A real-time terminal dashboard for monitoring git repositories.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Rich](https://img.shields.io/badge/rich-13+-green.svg)

## Overview

GitPulse provides a live-updating terminal interface showing:
- Current branch and repository status
- Latest commit information
- Recent commits table
- Today's file changes with diff statistics

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd gitpulse

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run from any git repository
python main.py

# Specify a different repository path
python main.py --path /path/to/repo

# Adjust refresh rate (default: 2.0 seconds)
python main.py --refresh 3.0
```

## Features

- **Live updates**: Automatically refreshes when files change (using watchdog)
- **Git status overview**: Shows staged, unstaged, and untracked file counts
- **Commit history**: Displays recent commits with author and timestamp
- **Today's changes**: Lists files modified today with add/delete statistics
- **Graceful exit**: Press Ctrl+C to exit cleanly

## Requirements

- Python 3.8+
- rich >= 13.0.0
- watchdog >= 3.0.0
- GitPython >= 3.0.0

## License

MIT License
