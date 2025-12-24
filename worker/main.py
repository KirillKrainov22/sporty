import asyncio
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

# Ensure the project root is on sys.path so `import worker...` works even when
# executed as a script from /app/worker.
for path in (PROJECT_ROOT, CURRENT_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from worker.consumers.activities import consume_activities


if __name__ == "__main__":
    asyncio.run(consume_activities())