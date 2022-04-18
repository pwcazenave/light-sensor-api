# Light sensor API

## Installation

These instructions assume a raspos host and a raspberry pi (any generation).

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
systemctl enable light.service
systemctl start light.service
```
