podman build --no-cache --rm --file Containerfile --tag vectorizing:demo .
podman run --interactive --tty vectorizing:demo
