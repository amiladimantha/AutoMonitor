"""
Entry point script to run AutoMonitor
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

LOCK_FILE = Path(__file__).parent / 'automonitor.lock'


def acquire_lock():
    """Prevent multiple bot instances from running at the same time."""
    if LOCK_FILE.exists():
        existing_pid = LOCK_FILE.read_text().strip()
        # Check if that process is still alive
        try:
            os.kill(int(existing_pid), 0)
            print(f"AutoMonitor is already running (PID {existing_pid}). Exiting.")
            sys.exit(0)
        except (OSError, ValueError):
            # Process is dead — stale lock file, safe to remove
            LOCK_FILE.unlink()
    LOCK_FILE.write_text(str(os.getpid()))


def release_lock():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


from src.main import main

if __name__ == "__main__":
    acquire_lock()
    try:
        main()
    finally:
        release_lock()
