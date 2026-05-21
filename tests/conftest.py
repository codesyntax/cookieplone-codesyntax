from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def downstream_repo_dir() -> Path:
    """Override the default downstream_repo_dir to point to this repository."""
    return Path(__file__).parent.parent.resolve()
