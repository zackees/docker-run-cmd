# Use the official Python 3.10 Alpine-based image
FROM python:3.10-alpine

# Install yt-dlp dependencies and yt-dlp itself
# Adding necessary packages including ffmpeg
RUN apk add --no-cache \
    ffmpeg \
    dos2unix \
    && pip install --no-cache-dir yt-dlp

# Set the working directory in the container
WORKDIR /host_dir

# Copy the entrypoint script into the container and make it executable
COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh && dos2unix ./entrypoint.sh

# Set the entrypoint to use /bin/sh
ENTRYPOINT ["sh", "-c", "yt-dlp", "\"$@\""]
