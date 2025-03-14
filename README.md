# td-ransomware-MTO

# Intro
# J'utilise GitLens pour gérer mes fichiers depuis VCode à l'aide de ma clé SSH

# Question 1
# Le chiffrement utilisé est le XOR. Il s'applique entre les données et la clé. On ne peut pas dire qu'il est sécurisé car la clé est souvent courte et réutilisée. Il est donc vulnérable à une attaque basé sur des statistiques. 

# Question 2
# Site internet utilisé : https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/
# https://docs.python.org/fr/3.8/library/secrets.html
# PBKDF2HMAC est conçu pour sécuriser les clés en appliquant plusieurs itérations de hachage et en utilisant HMAC. SI on hache le sel et la clé directement ce serait trop rapide car sans itérations donc vulnérable aux attaques (ex : brutforce)

# Question 3
# Il est préférable de vérifier si le fichier token.bin existe déjà pour éviter d'écraser un fichier existant et de perdre des données

# Question 4 
# On prend la clé fournie par la victime. On utilise cette clé avec le sel pour générer un nouveau token
# On compare ce nouveau token avec le token utilisé pour chiffrer
# Si les deux tokens sont identiques cela signifie que la clé est correcte.
