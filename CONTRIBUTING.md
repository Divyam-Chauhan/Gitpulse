# Contributing to GitPulse

Thanks for your interest in contributing to GitPulse! This guide will help you get started.

For basic project setup and usage, see the [README](README.md).

---

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/Gitpulse.git
   cd Gitpulse
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feat/your-feature-name
   ```

---

## How to Run

Run GitPulse from inside any git repository:

```bash
python main.py
```

Or point it at a specific repo:

```bash
python main.py --path /path/to/repo --refresh 3.0
```

Press `Ctrl+C` to exit.

---

## How to Report Bugs

Open a [GitHub Issue](https://github.com/Divyam-Chauhan/Gitpulse/issues) and include:

- A clear description of the bug
- Steps to reproduce it
- Expected vs actual behavior
- Your Python version (`python --version`) and OS

Use the **Bug Report** issue template if available.

---

## How to Submit a PR

1. Keep PRs focused — **one feature or fix per PR**
2. Use **conventional commit messages**:
   - `feat: add stash count to status panel`
   - `fix: handle empty repos gracefully`
   - `docs: update CONTRIBUTING.md`
   - `chore: clean up bare except blocks`
3. Reference the issue number in your PR description: `Closes #12`
4. Make sure `python main.py` runs without errors before submitting

---

## Code Style

- Follow **PEP 8**
- Keep it simple — readability over cleverness
- Add docstrings to new functions and classes
- Don't introduce new dependencies without discussing it first in an issue

---

## Good First Issues

New to open source? Start here. Each issue is small, scoped, and doesn't require understanding the full architecture.

---

### 1. Add `--version` flag to CLI

**What to do:** Add a `--version` argument to the argument parser that prints the current GitPulse version and exits.

**Files:** `main.py`, `config.py`
- Add a `VERSION = "1.0.0"` constant in `config.py`
- Add `parser.add_argument("--version", action="version", version=f"GitPulse {VERSION}")` in `parse_args()`

**Why beginner-friendly:** It's a one-liner in argparse — no logic changes, no UI changes. Great intro to the CLI layer.

---

### 2. Show total commit count in the Repository Status panel

**What to do:** Display the total number of commits on the current branch alongside the staged/unstaged/untracked counts in the top-left panel.

**Files:** `git_parser.py`, `ui.py`
- Add a `get_total_commit_count()` method to `GitParser` using `self.repo.iter_commits()`
- Wire it into `GitData` and display it in `_render_top_left()`

**Why beginner-friendly:** One new method + one new line in the UI. Follows the exact same pattern as `get_status_counts()`.

---

### 3. Handle empty repositories gracefully

**What to do:** When GitPulse is run in a freshly `git init`-ed repo with zero commits, it currently crashes because `self.repo.head.commit` throws. Show a friendly "No commits yet" state instead.

**Files:** `git_parser.py`
- Add a check for `self.repo.head.is_valid()` at the top of `get_status_counts()` (line 76 calls `self.repo.index.diff("HEAD")` which fails on empty repos)
- Return safe defaults when HEAD doesn't exist

**Why beginner-friendly:** It's a defensive check — add an `if` guard and return early. Good intro to edge-case handling.

---

### 4. Add color-coded status indicators (● / ○) instead of `[+] [~] [?]`

**What to do:** Replace the plain-text status markers in the Repository Status panel with colored circle symbols for a more polished look.

**Files:** `ui.py` (lines 86–91)
- Replace `"[+] "` → `"● "`, `"[~] "` → `"● "`, `"[?] "` → `"○ "` (keeping the existing color styles)

**Why beginner-friendly:** Pure cosmetic change in a single method (`_render_top_left`). No logic involved.

---

### 5. Add a `--no-watch` flag to disable filesystem watching

**What to do:** Add a CLI flag that disables the `watchdog` filesystem watcher, making GitPulse rely purely on its timed refresh loop. Useful on systems where `watchdog` has issues.

**Files:** `main.py`
- Add `--no-watch` boolean argument to `parse_args()`
- Conditionally skip `watcher.start()` and `watcher.has_changes()` based on the flag

**Why beginner-friendly:** It's just wrapping two existing lines in an `if` statement. No new modules or complex logic.

---

### 6. Truncate long branch names in the status panel

**What to do:** Feature branches like `feature/JIRA-12345-implement-user-authentication-flow` overflow the panel. Truncate branch names longer than 30 characters with `...`.

**Files:** `ui.py` (line 83)
- Before appending the branch name, check its length and truncate if needed:
  ```python
  branch_display = self.data.branch if len(self.data.branch) <= 30 else self.data.branch[:27] + "..."
  ```

**Why beginner-friendly:** Single-line string operation. Easy to test visually by just running the dashboard.

---

### 7. Add a "Stash count" indicator to the status panel

**What to do:** Show how many stashes exist (e.g., `Stashes: 3`) in the Repository Status panel. Many developers forget about stashed work.

**Files:** `git_parser.py`, `ui.py`
- Add a method: `def get_stash_count(self) -> int:` using `len(self.repo.git.stash("list").splitlines())` (returns 0 if empty)
- Add a line in `_render_top_left()` to display it

**Why beginner-friendly:** One tiny method + one UI line. Same pattern as staged/unstaged/untracked.

---

### 8. Bare `except:` cleanup in `get_today_changes()`

**What to do:** Line 129 of `git_parser.py` has a bare `except:` (no exception type specified). This silently swallows all errors including `KeyboardInterrupt` and `SystemExit`. Replace it with `except Exception:`.

**Files:** `git_parser.py` (line 129)
- Change `except:` → `except Exception:`

**Why beginner-friendly:** Literally a 1-word change. Great intro to Python best practices and contributing to open source. Good for someone making their very first PR ever.

---

### 9. Add a `CONTRIBUTING.md` file

This one's done — you're reading it! 🎉

---

### 10. Show an error message when `git` is not installed

**What to do:** If `git` is not installed or not in PATH, GitPulse crashes with a confusing `GitPython` traceback. Add a human-friendly error message at startup.

**Files:** `main.py`
- Before creating the `GitParser`, try running `subprocess.run(["git", "--version"])` and catch `FileNotFoundError`
- Print: `"Error: git is not installed or not found in PATH."` and `sys.exit(1)`

**Why beginner-friendly:** It's a simple try/except guard at the top of `main()`. Teaches error handling and UX thinking.
