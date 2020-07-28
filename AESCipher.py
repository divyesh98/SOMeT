import sys
import os
import random
import base64
from Crypto.Cipher import AES
from Crypto import Random

# importing the password based key distribution function, give more security
from Crypto.Protocol.KDF import PBKDF2

#imporing hash function for key generation
import hashlib

class AESCipher():

    BLOCK_SIZE = 16

    def __init__(self, secret_string, stego_type):

        self.raw = secret_string
        self.password = "You can't see me"
        self.stego = stego_type
        self.iv = ""
        self.bs = AES.block_size
        self.key = ""

    def generate_key(self):
        k = hashlib.sha256(self.password.encode()).digest()
        if self.stego == "DCT":
            text_file = open("secret/secretDCTAES.txt", "w")
            text_file.write(str(k))
            text_file.close

        elif self.stego == "Plain":
            text_file = open("secret/secretPlainAES.txt", "w")
            text_file.write(str(k))
            text_file.close
        return k

    
    def encrypt(self):
        self.raw = self._pad(self.raw)
        self.iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(self.iv + cipher.encrypt(self.raw.encode()))
        
    def decrypt(self):
        
        print(type(self.raw))
        self.raw = self.raw.encode("utf-8")
        self.raw = base64.b64decode(self.raw)
        print(self.raw, len(self.raw))
        self.iv = self.raw[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_cipher = cipher.decrypt(self.raw[AES.block_size:])
        return self._unpad(decrypted_cipher).decode('utf8')

    def _pad(self, s):
        return s + ((self.bs - (len(s) %  self.bs)) * chr(self.bs- (len(s) % self.bs)))

    def _unpad(self, s):
        return s[: -ord(s[len(s) - 1:])]
    
    def run(self, encrypt_decrypt):
        self.key = self.generate_key()
        
        if encrypt_decrypt == "Encrypt":
            encrypted_string = self.encrypt().decode("utf-8")
            print("Encrypted data is ", encrypted_string, len(encrypted_string),
                  type(encrypted_string))
            return encrypted_string
        else:
            decrypted_string = self.decrypt()
            print("Decrypted data is ", decrypted_string)
            return decrypted_string
