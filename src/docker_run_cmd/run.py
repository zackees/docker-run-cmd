

import os
import subprocess
import sys
import time
from pathlib import Path

# Define the Docker Desktop executable path for Windows
WIN_DOCKER_EXE = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"

def check_docker_running():
    """Check if Docker service is running."""
    result = os.system('docker ps')
    return result == 0

def start_docker_service():
    """Start Docker service depending on the OS."""
    if os.name == 'nt':  # Windows
        os.system(f'start "" "{WIN_DOCKER_EXE}"')
    elif os.name == 'posix':  # Unix-like
        os.system('open -a Docker')
    else:
        print("Unsupported operating system.")
        sys.exit(1)
    # Wait for Docker to start
    time.sleep(30)  # Adjust this as needed

def build_image(image_name, dockerfile_path):
    """Build the Docker image if it doesn't exist."""
    build_command = f'docker build -t {image_name} {os.path.dirname(dockerfile_path)}'
    os.system(build_command)

def remove_container(container_name):
    """Remove the existing container if it exists."""
    subprocess.run(f"docker rm -f {container_name}", shell=True, check=False, capture_output=True)
    # os.system(f'docker rm -f {container_name}')

def run_container(image_name: str, container_name: str, working_dir: str, host_volume: str, container_volume: str, cmd_args: list[str]) -> None:
    """Run the Docker container."""
    remove_container(container_name)
    run_command = (
        f'docker run --name {container_name} '
        f'-v "{host_volume}":"{container_volume}" '
        f'-w "//{working_dir}" {image_name} '
        + " ".join(cmd_args)
    )
    subprocess.run(run_command, shell=True, check=True)

def to_abs_path(path):
    """Convert Windows path to Unix path."""
    path = os.path.abspath(path)
    return path

def main(dockerfile: str, image_name: str, container_name: str, host_volume: str, container_volume: str, cmd_args: list[str], working_dir: str):
    if not check_docker_running():
        print("Docker is not running, attempting to start Docker...")
        start_docker_service()

    if not check_docker_running():
        print("Failed to start Docker. Please start Docker manually and try again.")
        sys.exit(1)

    print("Building Docker image...")
    build_image(image_name, dockerfile)

    print("Removing any existing container...")
    remove_container(container_name)

    print("Running new Docker container...")
    host_volume = to_abs_path(host_volume)
    # unix_container_volume = to_unix_abs_path(container_volume)
    run_container(image_name, container_name, to_abs_path(working_dir), host_volume, container_volume, cmd_args)

def unit_test() -> None:
    dockerfile = 'src/docker_run_cmd/Dockerfile'  # Replace with your actual Dockerfile path
    image_name = 'docker-yt-dlp'
    container_name = 'container-docker-yt-dlp'
    working_dir = 'src'  # Replace with your container's working directory
    host_volume = '.'  # Replace with your host volume
    container_volume = '/host_dir'  # Replace with your container volume
    cmd_args = ['--version']  # Replace with your command arguments

    # Convert paths and run main process
    dockerfile = to_abs_path(dockerfile)
    working_dir = to_abs_path(working_dir)
    main(dockerfile,
         image_name,
         container_name,
         host_volume,
         container_volume,
         cmd_args,
         working_dir)

if __name__ == "__main__":
    unit_test()