"""
Main entry point.
"""

import sys

from docker_run_cmd.run import unit_test


def main() -> int:
    """Main entry point."""
    unit_test()
    return 0


if __name__ == "__main__":
    sys.argv.append("Dockerfile")
    sys.argv.append("--")
    sys.argv.append("--version")
    sys.exit(unit_test())
