# Start isard kiosk
# llegir els usuaris juntament amb les ip
# afegir la clau i treure la contrasenya
from fabric import Connection

class SSHService:
    def __init__(self, url):
        self.url = url
        try: 
            config_ssh = {"password": "pirineus"}
            self.c = Connection(host=url, user="isard", connect_kwargs=config_ssh)
        except Exception as e:
            print(f"No connection: {e}")
    
    def __str__(self):
        return f"Connection is {self.url}"

    def run(self,cmd):
        self.c.run(cmd)

    
