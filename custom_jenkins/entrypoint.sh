#!/bin/bash
set -e

# Fix docker socket permissions at runtime
if [ -S /var/run/docker.sock ]; then
    chmod 666 /var/run/docker.sock
fi

# Drop privileges and start Jenkins as jenkins user
exec gosu jenkins /usr/bin/tini -- /usr/local/bin/jenkins.sh "$@"
