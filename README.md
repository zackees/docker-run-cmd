# docker-run-cmd

```bash
pip install run-docker-cmd
```

Run a self contained docker file representing an entry point. Useful for dockerizing
utility functions.

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)


Example dockerfile command:
```
# Use the official Python 3.10 Alpine-based image
FROM python:3.10-alpine

# Install yt-dlp dependencies and yt-dlp itself
# Adding necessary packages including ffmpeg
RUN apk add --no-cache \
    ffmpeg \
    dos2unix \
    && pip install --no-cache-dir yt-dlp ytdlp-brighteon

# Set the working directory in the container
WORKDIR /host_dir

# Build the entrypoint script in the container.
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'yt-dlp "$@"' >> /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint to use /bin/sh
ENTRYPOINT ["sh", "/entrypoint.sh"]
```

Now save this as mydockerfile

Now run it:

```bash
run-docker-cmd mydockerfile
```

## Docker commands

Self contained dockerfile's representing a command to be run. No external dependencies. The current working directory will be mapped into the container as /host_dir

# Develope

To develop software, run `. ./activate.sh`

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.
