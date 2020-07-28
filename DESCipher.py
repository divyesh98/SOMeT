import sys
import os
import random
import base64
from Crypto.Cipher import DES
from Crypto.Cipher import DES3
from Crypto import Random
import pyDes

# importing the password based key distribution function, give more security
from Crypto.Protocol.KDF import PBKDF2

#imporing hash function for key generation
import hashlib

# DES is single DES
# DES3 is triple DES

class DESCipher():

    #BLOCK_SIZE = 8

    def __init__(self, secret_string, stego_type):

        self.raw = secret_string
        self.password = "Let's party hard"
        self.stego = stego_type
        self.iv = ""
        self.bs = DES3.block_size
        self.key = ""

    def generate_key(self):
        k = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad =
                             None, padmode = pyDes.PAD_PKCS5)
        if self.stego == "DCT":
            text_file = open("secret/secretDCTDES.txt", "w")
            text_file.write(str(k))
            text_file.close

        elif self.stego == "Plain":
            text_file = open("secret/secretPlainDES.txt", "w")
            text_file.write(str(k))
            text_file.close
        return k
        
    '''    k = hashlib.sha256(self.password.encode()).digest()
        if self.stego == "DCT":
            text_file = open("secret/secretDCTDES3.txt", "w")
            text_file.write(str(k))
            text_file.close

        elif self.stego == "Plain":
            text_file = open("secret/secretPlainDES3.txt", "w")
            text_file.write(str(k))
            text_file.close
        return k

    
    def encrypt(self):
        self.raw = self._pad(self.raw)
        self.iv = Random.new().read(DES3.block_size)
        cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        return base64.b64encode(self.iv + cipher.encrypt(self.raw.encode()))
        
    def decrypt(self):
        
        print(type(self.raw))
        self.raw = self.raw.encode("utf-8")
        self.raw = base64.b64decode(self.raw)
        print(self.raw, len(self.raw))
        self.iv = self.raw[:DES3.block_size]
        cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        decrypted_cipher = cipher.decrypt(self.raw[DES3.block_size:])
        return self._unpad(decrypted_cipher).decode('utf8')

    def _pad(self, s):
        return s + ((self.bs - (len(s) %  self.bs)) * chr(self.bs- (len(s) % self.bs)))

    def _unpad(self, s):
        return s[: -ord(s[len(s) - 1:])]
    '''
    def run(self, encrypt_decrypt):
        self.key = self.generate_key()
        
        if encrypt_decrypt == "Encrypt":
            #encrypted_string = self.encrypt().decode("utf-8")
            encrypted_string = self.key.encrypt(self.raw)
            print("Encrypted data is ", encrypted_string, len(encrypted_string),
                  type(encrypted_string))
            return encrypted_string.decode('latin-1')
        
        else:

            if self.stego == "DCT":
                key_file = open("secret/secretDCTDES.txt", "r")
                self.key = key_file.readline()
                key_file.close()

            elif self.stego == "Plain":
                key_file = open("secret/secretPlainDES.txt", "r")
                self.key = key_file.readline()
                key_file.close()

            self.key = self.generate_key()
            string = self.raw.encode('latin-1')
            decrypted_string = self.key.decrypt(string).decode('latin-1')
            
            print("Decrypted data is ", decrypted_string)
            return decrypted_string
