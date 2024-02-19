"""
Unit test file.
"""

import os
import unittest

# COMMAND = "docker-run-cmd --dockerfile Dockerfile --name docker-yt-dlp --host-dir . --container-dir /host_dir -- --help"
COMMAND = "docker-run-cmd Dockerfile -- --help"

HERE = os.path.abspath(os.path.dirname(__file__))


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        # rtn = os.system(COMMAND)
        # self.assertEqual(0, rtn)
        os.chdir(HERE)
        rtn = os.system(f"{COMMAND}")
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
