"""
Main entry point.
"""

import sys

from docker_run_cmd.api import check_docker_running, start_docker_service


def main() -> int:
    """Main entry point."""
    if not check_docker_running():
        print("Starting docker server...")
        start_docker_service()
        return 0
    print("Docker server is already running.")
    return 0


if __name__ == "__main__":
    raise sys.exit(main())
