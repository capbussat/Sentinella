# Sentinella
Sentinella has a Python GUI written with ttkbootstrap and some Bash scripts which can start remotely a Chomium Browser with restricted kiosk like policies or close access to internet to several computers in a LAN.

It is in current development.

# Purpose:
The purpose of this software is to restrict access from a student class to Internet or allow access only to a few sites. It aims to be compatible with using Veyon at the same time.
- Create  a new user with restrictions like (install-kiosk.sh)
- Start a Chromium browser with restriction policies and start Chromium with restrictions (install-chromium-policies.s).
- Close outgoing internet traffik except for essential services (DHCP, DNS, Veyon ...) and a list of allowed domain with Sentinella script by using UFW (Linux Uncomplicated FireWall). Requires  install-sentinella.sh.

# Python GUI Requires:
Requires Python, SSH access on remote computers,  Bash scripting and UFW installation for Linux firewall, so only can administer Linux computers.
The ttkbootstrap and fabric modules (for SSH) are necessary in a Python environment. Pyyaml is used to get settings and Pyinstaller to create a distributable file for the GUI.
Should be installed on master computer.

# Development installation on LInux computer:

git clone https://github.com/capbussat/Sentinella

cd Sentinella

# Create a Python environment to create a Pyhton GUI
sudo python3 -m venv .venv

source .venv/bin/activate

pip install ttkbootstrap fabric pyyaml pyinstaller\

python3 senti.py\

Create a senti file to distribute the Python GUI:

pyinstaller --onefile --noconsole senti.py

Disable Python environment with: deactivate.

# Scripts for Clients
There are three separate installation scripts. You do not need to use all of them.\
Use:

# Allow file
Edit the allow file with a list of allowed domain. One domain only for line.
Sentinella script requires dig command to translate domains to IPs.
This file is placed by installation script in clients. 

# Install on clients

sudo chmod +x install-kiosk.sh\
sudo ./install-kiosk.sh\
sudo chmod +x install-chromium-policies.sh\
sudo ./install-chromium-policies.sh\
sudo chmod +x install-sentinella.sh\
sudo ./install-sentinella.sh

# You do not need to install anything if you use:
sudo chmod +x onsentinella.sh\
sudo chmod +x offsentinella.sh\
./onsentinella.sh\
Restricts internet access.\
./offsentinella.sh\
Allows internet access.
