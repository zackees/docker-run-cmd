import os
import shutil
from pathlib import Path
from string import Template
from tempfile import TemporaryDirectory

HERE = Path(__file__).parent
WIN_DOCKER_EXE = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
DOCKER_COMPOSE_TEMPLATE = HERE / "assets" / "docker-compose-template.yml"


def run(dockerfile: Path, cwd: Path, cmd_list: list[str]) -> None:
    """Run the Docker container."""
    with TemporaryDirectory() as tempdir:
        td = Path(tempdir)
        print(f"Temporary directory: {td}")
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
            os.system("docker-compose up --exit-code-from app")
        finally:
            os.chdir(prev_dir)
