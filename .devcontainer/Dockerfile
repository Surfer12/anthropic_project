# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/devcontainers/base:bullseye

# Install any needed packages specified in requirements.txt
# (Create a requirements.txt file if you have dependencies)
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# Add any other setup steps here (installing system packages, etc.)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (needed for Docker-outside-of-Docker)
RUN curl -fsSL https://get.docker.com -o get-docker.sh \
    && sh get-docker.sh \
    && rm get-docker.sh

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set a default user.  This is a good practice.
# USER youruser

# [Optional] If you have specific user/group ID requirements, set them here:
# ARG USER_UID=1000
# ARG USER_GID=$USER_UID
# RUN groupadd --gid $USER_GID youruser \
#     && useradd --uid $USER_UID --gid $USER_GID -m youruser 