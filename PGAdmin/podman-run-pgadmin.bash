#!/bin/bash

# Define the container name
CONTAINER_NAME="pgadmin_container"

# Check if the container exists
if podman container exists "${CONTAINER_NAME}"; then
    echo "Container '${CONTAINER_NAME}' exists."
    # Check if it's running
    if [[ "$(podman inspect -f '{{.State.Status}}' ${CONTAINER_NAME})" == "running" ]]; then
        echo "Container '${CONTAINER_NAME}' is already running."
    else
        echo "Starting container '${CONTAINER_NAME}'..."
        podman start "${CONTAINER_NAME}"
    fi
else
    echo "Creating and starting container '${CONTAINER_NAME}'..."
    podman run --name "$CONTAINER_NAME" \
        --detach \
        --publish "8080:80" \
        --publish "8081:443" \
        --env PGADMIN_DEFAULT_EMAIL=pgadmin@localhost \
        --env PGADMIN_DEFAULT_PASSWORD="pgsecret" \
        --env PGADMIN_CONFIG_CHECK_EMAIL_DELIVERABILITY=False \
        --env PGADMIN_CONFIG_GLOBALLY_DELIVERABLE=False \
        --volume pgadmin_data:/var/lib/pgadmin \
        --volume "$(pwd)/servers.json:/pgadmin4/servers.json" \
        --restart=always \
        docker.io/dpage/pgadmin4:9.10.0
fi

podman logs --follow "${CONTAINER_NAME}"
