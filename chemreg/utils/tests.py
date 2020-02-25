import subprocess

from django.conf import settings


def test_lint():
    """Test codebase has no linting errors."""
    returncode = subprocess.call(
        ["flake8"],
        cwd=settings.ROOT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    assert not returncode, "Flake8 found linting errors"
