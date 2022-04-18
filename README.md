# Light sensor API

## Installation

These instructions assume a raspos host and a raspberry pi (any generation).

### Quick start
```bash
apt install python3-venv
python3 -m venv venv --system-site-packages
. venv/bin/activate
pip3 install -r requirements.txt
# Open up the firewall if you want to access it directly via
sudo ufw allow 8000/tcp
cd app
HOST=0.0.0.0 python3 main.py
```

