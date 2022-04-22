podman stop light
podman rm light
podman build --tag light:latest .
# --group-add keep-groups means we inherit groups from the user running podman
# which means we can read /dev/spidev0.0. See:
#    https://www.redhat.com/sysadmin/files-devices-podman
# for details.
podman run --detach --publish 8000:8000 --device /dev/spidev0.0:/dev/spidev0.0 --group-add keep-groups --name light localhost/light:latest
sleep 1
podman logs light
