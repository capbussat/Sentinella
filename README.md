# Sentinella
Sentinella has a Python GUI written with ttkbootstrap and some Bash scripts which aims to restrict access to internet to several computers in a LAN.  
For example it can restric acces to internet except a few allowed sites and impose policy restriction to Chromium and Firefox browsers.

It is in current development, only for Linux desktops.  

# Purpose:
The purpose of this software is to restrict access from a student class to Internet and allow access only to a few sites. 
It aims to be compatible with using Veyon at the same time so keeps open required ports on clients computers.  
- Current versions applies policies to Chromium and Firefox browsers.  
- Close outgoing internet traffik except for essential services (DHCP, DNS, Veyon ...) and domains listed on allow file.  
- Check students can access internet (simple ping to google).  

## Python controller GUI Requires:
Requires Python. Uses a ssh client to access student computers.

## Student computers
Requires a installed Sentinella service and UFW (Uncomplicated Linux firewall) so only can run on Linux computers.


## Development
Requires a few Python non standard modules like ttkbootstrap, fabric, pyyaml and pyinstaller.  

### Development installation on LInux computer:
git clone https://github.com/capbussat/Sentinella

cd Sentinella/controller  (teacher computer)

cd Sentinella/client (student computer)

### Create a Python environment to create the controller Pyhton GUI

cd Sentinella  

sudo python3 -m venv .venv

source .venv/bin/activate

pip install ttkbootstrap fabric pyyaml pyinstaller\

python3 controller/senti.py

# Distribute executable for controller computer
Create a senti file to distribute the Python GUI:

pyinstaller --onefile --noconsole senti.py  

Disable Python environment with deactivate.

### Scripts for Clients
Use install-sentinella.sh to set up the clients.  

cd Sentinella/client  
sudo chmod +x install-sentinella.sh  
sudo ./install-sentinella.sh  

### Allow file
Edit the allow file with a list of allowed domains. One domain for line. allow file is copied by the installation script.  
You should modify the allow file before the install. If you modify the allow file you can repeat the install process.
Sentinella script uses the "dig" command to translate domains to IPs.

### Scripts for controller
Use install-sentinella-gui.sh to set up the controller computer.  

cd Sentinella/controller  
sudo chmod +x install-sentinella-gui.sh  
sudo ./install-sentinella-gui.sh  


