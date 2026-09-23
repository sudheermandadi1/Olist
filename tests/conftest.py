import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("pytest_tests")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    LOG_DIR / "pytest.log",
    mode="a",
    encoding="utf-8",
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.propagate = False