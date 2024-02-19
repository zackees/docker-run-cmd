import sys
import os
import argparse
import time
import subprocess
from typing import Optional
import docker
from docker.errors import DockerException
from docker.models.containers import Container

from docker_run_cmd.docker_helper import check_docker_running, start_docker_service, get_container, image_exists, build_image

# Define your image and container names
IMAGE_NAME: str = 'docker-yt-dlp'
CONTAINER_NAME: str = 'container-docker-yt-dlp'

HOST_VOLUME = os.getcwd()
    
def parse_args() -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(description="Run YouTube-DL in a Docker container.")
    parser.add_argument("dockerfile", help="Path to the Dockerfile")
    args, other_args = parser.parse_known_args()
    return args, other_args

def run(dockerfile: str, imagename: str, containername: str, hostvolume: str, remotevolume: str, cmd_args: list[str]) -> None:
    if not check_docker_running():
        start_docker_service()
    try:
        client: docker.DockerClient = docker.from_env()
    except DockerException:
        print("Docker is not running. Please start Docker and try again.")
        return
    
    build_image(client, imagename, dockerfile=dockerfile)
    if not image_exists(client, imagename):
        print("Image does not exist, pulling...")
        client.images.pull(imagename)
    
    container: Optional[Container] = get_container(client, containername)
    if container:
        print("Removing existing container...")
        container.remove(force=True)  # Force removal if running or stopped
    
    print("Running Docker container with the necessary arguments...")
    cmd_str = subprocess.list2cmdline(cmd_args)
    volumes = {hostvolume: {'bind': remotevolume, 'mode': 'rw'}}
    container = client.containers.run(
        imagename, 
        cmd_str,
        name=containername,
        volumes=volumes,
        detach=True,
        auto_remove=True
    )

    for log in container.logs(stream=True):
        print(log.decode("utf-8"), end="")

def unit_test() -> None:
    args, other_args = parse_args()
    dockerfile = args.dockerfile
    run(dockerfile=dockerfile,
        imagename=IMAGE_NAME,
        containername=CONTAINER_NAME,
        hostvolume=HOST_VOLUME,
        remotevolume="/host_dir",
        cmd_args=other_args)

if __name__ == "__main__":
    sys.argv.append("Dockerfile")
    sys.argv.append("--")
    sys.argv.append("--version")
    unit_test()
