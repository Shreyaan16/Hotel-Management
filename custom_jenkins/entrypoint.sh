#!/bin/bash
set -e

# Fix docker socket GID mismatch at runtime
if [ -S /var/run/docker.sock ]; then
    DOCKER_SOCK_GID=$(stat -c '%g' /var/run/docker.sock)
    groupmod -g "$DOCKER_SOCK_GID" docker
    usermod -aG docker jenkins
fi

# Drop privileges and start Jenkins as jenkins user
exec gosu jenkins /usr/bin/tini -- /usr/local/bin/jenkins.sh "$@"
