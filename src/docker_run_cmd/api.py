# pylint: disable=too-many-locals

import os
import shutil
import sys
import time
from pathlib import Path
from string import Template
from tempfile import TemporaryDirectory

from download import download

HERE = Path(__file__).parent
WIN_DOCKER_EXE = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
DOCKER_COMPOSE_TEMPLATE = HERE / "assets" / "docker-compose-template.yml"


def check_docker_running():
    """Check if Docker service is running."""
    result = os.system("docker ps")
    return result == 0


def start_docker_service():
    """Start Docker service depending on the OS."""
    if os.name == "nt":  # Windows
        os.system(f'start "" "{WIN_DOCKER_EXE}"')
    elif os.name == "posix":  # Unix-like
        os.system("open -a Docker")
    else:
        print("Unsupported operating system.")
        sys.exit(1)
    # Wait for Docker to start
    time.sleep(30)  # Adjust this as needed


def remove_existing_container(container_name):
    """Remove existing Docker container with the given name."""
    result = os.system(f"docker inspect {container_name}")
    if result == 0:  # Container exists
        print(f"Removing existing container named {container_name}...")
        os.system(f"docker rm -f {container_name}")


def docker_run(
    name: str, dockerfile_or_url: str, cwd: Path, cmd_list: list[str]
) -> int:
    """Run the Docker container."""
    if not shutil.which("docker-compose"):
        print("docker-compose not found. Please install it.")
        return 1
    if not shutil.which("docker"):
        print("docker not found. Please install it.")
        return 1
    if not check_docker_running():
        start_docker_service()

    with TemporaryDirectory() as tempdir:
        td = Path(tempdir)
        print(f"Temporary directory: {td}")
        dockerfile = Path(dockerfile_or_url)
        if not dockerfile.exists():
            # download the file
            print(f"Downloading Dockerfile from {dockerfile_or_url}...")
            dockerfile = download(url=dockerfile_or_url, path=tempdir, replace=True)
            dockerfile = Path(dockerfile)
        docker_compose_content = DOCKER_COMPOSE_TEMPLATE.read_text(encoding="utf-8")
        # add quotes to each object if they are not already quoted
        cmd_list = [f'"{cmd}"' for cmd in cmd_list]
        cmd_str = "[" + ",".join(cmd_list) + "]"
        image_name = f"docker-run-cmd-{name}-image"
        container_name = f"docker-run-cmd-{name}-container"
        docker_compose_content = Template(docker_compose_content).substitute(
            dockerfile=dockerfile.name,
            hostdir=cwd.resolve(),
            command=cmd_str,
            image_name=image_name,
            container_name=container_name,
        )
        docker_compose_file = td / "docker-compose.yml"
        docker_compose_file.write_text(docker_compose_content, encoding="utf-8")
        # shutil.copy(DOCKER_COMPOSE_TEMPLATE, docker_compose_file)
        print(f"docker-compose file: {docker_compose_file}")
        target_dockerfile = td / "Dockerfile"
        # if not the same path then copy
        contents = dockerfile.read_text(encoding="utf-8")
        target_dockerfile.write_text(contents, encoding="utf-8")
        print(f"Dockerfile: {dockerfile}")
        print()
        prev_dir = Path.cwd()
        os.chdir(td)
        rtn = 0
        try:
            os.system("docker-compose down --rmi all")
            # now docker compose run the app
            print("Building the Docker image...")
            os.system("docker-compose build")
            remove_existing_container(container_name)
            print("Running the Docker container...")
            # Add -d to run in detached mode, if interactive mode is not needed.
            os.system("docker network prune --force")
            rtn = os.system("docker-compose up --no-log-prefix --exit-code-from app")
            os.system("docker network prune --force")
            print("DONE")
        finally:
            os.chdir(prev_dir)
        return rtn
