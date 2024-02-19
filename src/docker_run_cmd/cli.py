"""
Main entry point.
"""

import sys

from docker_run_cmd.run import unit_test

if __name__ == "__main__":
    sys.argv.append("Dockerfile")
    sys.argv.append("--")
    sys.argv.append("--version")
    sys.exit(unit_test())
