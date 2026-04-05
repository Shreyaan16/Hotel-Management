#!/bin/bash
# Fix docker socket GID mismatch at runtime
DOCKER_SOCK_GID=$(stat -c '%g' /var/run/docker.sock)
CURRENT_GID=$(getent group docker | cut -d: -f3)

if [ "$DOCKER_SOCK_GID" != "$CURRENT_GID" ]; then
    groupmod -g "$DOCKER_SOCK_GID" docker
fi

exec /usr/bin/tini -- /usr/local/bin/jenkins.sh "$@"
