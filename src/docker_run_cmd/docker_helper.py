import sys
import os
import argparse
import time
import subprocess
from typing import Optional
import docker
from docker.errors import DockerException
from docker.models.containers import Container
import docker.errors


HOST_VOLUME = os.getcwd()

WIN_DOCKER_EXE = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"


def check_docker_running() -> bool:
    """Check if Docker service is running on Windows."""
    cmd = "docker ps"
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_docker_service() -> None:
    """Start Docker service on Windows."""
    if os.name == 'nt':  # Checks if the operating system is Windows
        print("Starting Docker service...")
        subprocess.run(["start", "", WIN_DOCKER_EXE], shell=True, capture_output=True, text=True, check=True)  # shell=True for Windows
        print("Waiting for Docker to start...")
    else:  # For macOS and Linux (Ubuntu)
        print("Starting Docker service...")
        subprocess.run(["open", "-a", "Docker"], capture_output=True, text=True, check=True)  # macOS specific
        # For Linux, Docker typically runs as a service already, so you might not need to start it manually.

    # Wait for Docker to start. Adjust the sleep time as needed.
    now = time.time()
    future_time = now + 30  # 30 seconds wait time
    while time.time() < future_time:
        if check_docker_running():
            print("\nDocker started successfully.")
            return
        time.sleep(1)
        print(".", end="", flush=True)
    raise OSError("Docker failed to start after waiting.")

def get_container(client: docker.DockerClient, container_name: str) -> Optional[Container]:
    try:
        return client.containers.get(container_name)
    except docker.errors.NotFound:
        return None

def build_image(client: docker.DockerClient, image_name: str, dockerfile: str) -> None:
    """Build Docker image if it doesn't exist."""
    try:
        client.images.get(image_name)
    except docker.errors.ImageNotFound:
        print("Image does not exist, building...")
        dirpath = ""
        if os.path.isfile(dockerfile):
            dirpath = os.path.dirname(dockerfile)
        else:
            dirpath = dockerfile
        dirpath = os.path.abspath(dirpath)
        client.images.build(path=dirpath, tag=image_name)

def image_exists(client: docker.DockerClient, image_name: str) -> bool:
    try:
        client.images.get(image_name)
        return True
    except docker.errors.ImageNotFound:
        return False