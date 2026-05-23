# Sentinella
Sentinella bash scripts establish Chomium Browser policies or close access to internet.

# Create  a user with restrictions (Kiosk)
# Open a Chromium browser with restriction policies
# Close outgoing access to Internet, 
Close otgoing internet traffik except for essential services and a list of allowed domain with Sentinella script by using UFW (Linux Uncomplicated FireWall).

There are three separate installation scripts use:

git clone https://github.com/capbussat/Sentinella/\
cd Sentinella\
Edit allow file and place a allowed domain in each line\
sudo chmod +x install-kiosk.sh\
sudo ./install-kiosk.sh\
sudo chmod +x install-chromium-policies.sh\
sudo ./install-chromium-policies.sh\
sudo chmod +x install-sentinella.sh\
sudo ./install-sentinella.sh
