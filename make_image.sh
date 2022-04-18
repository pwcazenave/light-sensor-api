podman stop light
podman rm light
podman build --tag light:latest .
podman push --tls-verify=false localhost/light:latest pod:5443/light:latest
podman run -dt -p 8008:8008 --name light localhost/light:latest
sleep 1
podman logs light
