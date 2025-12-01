#!/bin/bash

# Define the container name
CONTAINER_NAME="pgvector_container"

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
    podman run --name "${CONTAINER_NAME}" \
        -d \
        -p 5432:5432 \
        -e POSTGRES_DB=rag_db \
        -e POSTGRES_USER=rag_user \
        -e POSTGRES_PASSWORD=rag_password \
        docker.io/pgvector/pgvector
fi
