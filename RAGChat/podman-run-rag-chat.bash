podman build --no-cache --rm --file Containerfile --tag ragchat:demo .
podman run --interactive --tty ragchat:demo
