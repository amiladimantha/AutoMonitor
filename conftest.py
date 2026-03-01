import sys
from pathlib import Path

# Make sure the project root is on sys.path so `src.*` imports resolve
sys.path.insert(0, str(Path(__file__).parent))
