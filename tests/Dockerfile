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

RUN chmod 777 /host_dir

# Set the entrypoint to use /bin/sh
ENTRYPOINT ["sh", "/entrypoint.sh"]
