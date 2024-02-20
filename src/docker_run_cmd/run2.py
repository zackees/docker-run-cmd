import os
import shutil
from pathlib import Path
from string import Template
from tempfile import TemporaryDirectory
from download import download
import time
import sys


HERE = Path(__file__).parent
WIN_DOCKER_EXE = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
DOCKER_COMPOSE_TEMPLATE = HERE / "assets" / "docker-compose-template.yml"


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

def remove_existing_container(container_name):
    """Remove existing Docker container with the given name."""
    result = os.system(f'docker inspect {container_name}')
    if result == 0:  # Container exists
        print(f"Removing existing container named {container_name}...")
        os.system(f'docker rm -f {container_name}')

def run(dockerfile_or_url: str, cwd: Path, cmd_list: list[str]) -> None:
    """Run the Docker container."""
    if not shutil.which("docker-compose"):
        print("docker-compose not found. Please install it.")
        return
    if not shutil.which("docker"):
        print("docker not found. Please install it.")
        return
    if not check_docker_running():
        start_docker_service()
    # test if dockerfile_or_url is a file


    with TemporaryDirectory() as tempdir:
        td = Path(tempdir)
        print(f"Temporary directory: {td}")
        dockerfile = Path(dockerfile_or_url)
        if not dockerfile.exists():
            # download the file
            print(f"Downloading Dockerfile from {dockerfile_or_url}...")
            dockerfile = download(dockerfile_or_url, tempdir, replace=True)
        docker_compose_content = DOCKER_COMPOSE_TEMPLATE.read_text(encoding="utf-8")
        cmd_str = "[" + ",".join(cmd_list) + "]"
        docker_compose_content = Template(docker_compose_content).substitute(
            dockerfile=dockerfile.name,
            hostdir=cwd.resolve(),
            command=cmd_str,
        )
        docker_compose_file = td / "docker-compose.yml"
        docker_compose_file.write_text(docker_compose_content, encoding="utf-8")
        # shutil.copy(DOCKER_COMPOSE_TEMPLATE, docker_compose_file)
        print(f"docker-compose file: {docker_compose_file}")
        shutil.copy(dockerfile, td / "Dockerfile")
        print(f"Dockerfile: {dockerfile}")
        print()
        prev_dir = Path.cwd()
        os.chdir(td)
        try:
            os.system("docker-compose down --rmi all")
            # now docker compose run the app
            print("Building the Docker image...")
            os.system("docker-compose build")
            remove_existing_container('my_custom_container_name')
            print("Running the Docker container...")
            # Add -d to run in detached mode, if interactive mode is not needed.
            os.system("docker-compose up --no-log-prefix --exit-code-from app")
        finally:
            os.chdir(prev_dir)
