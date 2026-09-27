from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def masterpw_set(salt, password):
          kdf = Argon2id(
                    salt=salt,
                    length=32,
                    iterations=3,
                    lanes=4,
                    memory_cost=262144, # 256 MB
          )
          key = kdf.derive(password.encode())
          aes = AESGCM(key)
          return aes


def Verschlüsselung(password_en, aes, nonce): 

          ciphertext = aes.encrypt(
                    nonce,
                    password_en.encode(), #String -> Bytes
                    None
          )

          return ciphertext

def Entschlüsselung(nonce_de, ciphertextdb, aes):

     plaintext = aes.decrypt(
                    nonce_de,
                    ciphertextdb,
                    None
               )
     return plaintext.decode()






