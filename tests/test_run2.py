"""
Unit test file.
"""

import unittest
from pathlib import Path

from docker_run_cmd.run2 import run

HERE = Path(__file__).parent
PROJECT_DIR = HERE.parent
DOCKER_FILE = PROJECT_DIR / "src" / "docker_run_cmd" / "Dockerfile"

assert DOCKER_FILE.exists(), f"Dockerfile not found: {DOCKER_FILE}"


class MainTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skip("Skip this test")
    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        run(name="yt-dlp-docker", dockerfile_or_url=DOCKER_FILE, cwd=PROJECT_DIR / "tmp", cmd_list=["--help"])
        print()

    # video https://www.youtube.com/watch?v=mh_hNvGTmIg
    @unittest.skip("Skip this test")
    def test_url(self) -> None:
        url = "https://www.youtube.com/watch?v=mh_hNvGTmIg"
        run(name="yt-dlp-docker", dockerfile_or_url=DOCKER_FILE, cwd=PROJECT_DIR / "tmp", cmd_list=[url])

    # https://www.brighteon.com/f77d70c8-f5a9-44fa-8125-dc3a6ac85643
    def test_url2(self) -> None:
        url = "https://www.brighteon.com/f77d70c8-f5a9-44fa-8125-dc3a6ac85643"
        run(name="yt-dlp-docker", dockerfile_or_url=DOCKER_FILE, cwd=PROJECT_DIR / "tmp", cmd_list=[url])


if __name__ == "__main__":
    unittest.main()
