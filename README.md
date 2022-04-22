# Light sensor API

## Hardware

I've written this with two light sensor configurations in mind:

1. https://pimylifeup.com/raspberry-pi-light-sensor/
1. https://tutorials-raspberrypi.com/photoresistor-brightness-light-sensor-with-raspberry-pi/ (and https://tutorials-raspberrypi.com/mcp3008-read-out-analog-signals-on-the-raspberry-pi/)

The former uses the photoresistor to time how long it takes to charge a capacitor with the light resistor in the circuit. The latter converts the light resistor values from analog to digital.


## Installation

These instructions assume a raspos host and a raspberry pi (any generation).

### Enable SPI

1. `sudo raspi-config`
1. Interface options > I4 SPI > Enabled
1. Reboot

### Quick start

```bash
apt install python3-venv
python3 -m venv venv --system-site-packages
. venv/bin/activate
pip3 install -r requirements.txt
# Open up the firewall
sudo ufw allow 8000/tcp
cd app
gunicorn --workers=1 --bind 0.0.0.0:8000 main:app
```

### systemd

As root:

```bash
cd /opt
git clone git@gitea:pica/light
cp /opt/light/systemd/light.service /etc/systemd/system/light.service
chmod 644 /etc/systemd/system/light.service
cd light
apt install python3-venv
python3 -m venv venv --system-site-packages
. venv/bin/activate
pip3 install -r requirements.txt
ufw allow 8000/tcp
systemctl daemon-reload
systemctl enable --now light.service
```

## Usage

Simplest way to use the API is to just curl the relevant endpoints, which are:

### Timed

The lightness is measured here as number of iterations needed to go from low to high on the resistor. Hence, a lower value is a higher light intensity (brighter).

* `/api/v1/timed/current`
* `/api/v1/timed/last/<period>`, where `<period>` is some integer number of seconds

### Analog to digital

This uses the MCP3008 to convert the analog signal to a digital one. Here, a low value is dark, high is light.

* `/api/v1/analog/current`
* `/api/v1/analog/last/<period>`, where `<period>` is some integer number of seconds

For example to fetch the current instantaneous analog value:

`curl http://example.com:8000/api/v1/analog/current | jq .current`

To average over 60 seconds:

`curl http://example.com:8000/api/v1/analog/last/60 | jq`
