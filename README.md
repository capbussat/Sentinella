# Sentinella
Sentinella has a Python GUI written with Flet and some Bash scripts which can start remotely a Chomium Browser with restricted kiosk like policies or close access to internet to several computers in a LAN.

It is in current development.

# Purpose:
The purpose of this software is to restrict access from a student class to internet or restrict access to a few sites. It aims to be compatible with using Veyon at the same time.
- Create  a new user with restrictions like 
- Start a Chromium browser with restriction policies and start Chromium with restrictions.
- Close outgoing access to Internet.
- Close outgoing internet traffik except for essential services (DHCP, DNS, Veyon ...) and a list of allowed domain with Sentinella script by using UFW (Linux Uncomplicated FireWall).

# Requires:
Requires Python, SSH access on remote computers, UFW installation for Linux firewall and Bash scripting, so only Works in remote Linux computers.
The Flet Python GUI can be used from any OS supported by Python ad Flet.

# Scripts
There are three separate installation scripts. You do not need to use all of them.\
Use:

git clone https://github.com/capbussat/Sentinella;
cd Sentinella

# Allow file
Edit allow file and place a allowed domain in each line
# Install and run
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

# Python Flet GUI
Should be installed on master computer.