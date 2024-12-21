import os

# Générer une clé secrète
secret_key = os.urandom(32).hex()  # 32 bytes = 64 caractères hexadécimaux
print(f"Clé secrète générée : {secret_key}")
