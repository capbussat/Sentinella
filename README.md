# Sentinella
Sentinella bash scripts establish Chomium Browser policies or close access to internet.

- Create  a new user with restrictions (Kiosk)
- Set Chromium browser with restriction policies and start Chromium with restrictions.
- Close outgoing access to Internet.
Close outgoing internet traffik except for essential services (DHCP, DNS, Veyon ...) and a list of allowed domain with Sentinella script by using UFW (Linux Uncomplicated FireWall).

There are three separate installation scripts. You do not need to use all of them.\
Use:

git clone https://github.com/capbussat/Sentinella/\
cd Sentinella\
# Allow file
Edit allow file and place a allowed domain in each line\
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
Allows internet access.\
