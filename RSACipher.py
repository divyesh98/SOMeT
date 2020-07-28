from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode

hash = "SHA256"

class RSACipher():
    
    def __init__(self, secret_string, stego_type):

        self.text = secret_string
        self.stego = stego_type
        self.private_key = ""
        self.public_key = ""
        self.key = ""

    def key_generator(self):

        key = RSA.generate(1024)

        print(type(key))
        
        if self.stego == "DCT":
            k = key.publickey().exportKey('PEM')
            text_file = open("secret/secretDCT_RSA_private.pem", "wb")
            text_file.write(key.exportKey('PEM'))
            text_file.close()

        elif self.stego == "Plain":
            k = key.publickey().exportKey('PEM')
            text_file = open("secret/secretPlain_RSA_private.pem", "wb")
            text_file.write(key.exportKey('PEM'))
            text_file.close()
            
        return k
    
    def run(self, encrypt_decrypt):

        if encrypt_decrypt == "Encrypt":
            self.public_key = RSA.importKey(self.key_generator())
            self.public_key = PKCS1_OAEP.new(self.public_key)

            print(self.public_key, type(self.public_key))

            encrypted_string = self.public_key.encrypt(self.text.encode())

            print("Encrypted data is ", encrypted_string, len(encrypted_string),
                  type(encrypted_string))

            print(encrypted_string.decode('latin-1'), len(encrypted_string.decode('latin-1')))
            return encrypted_string.decode('latin-1')

        else:
            print(self.text, len(self.text))
            if self.stego == "DCT":
                key_file = open("secret/secretDCT_RSA_private.pem", "rb")
                self.private_key = key_file.read()
                key_file.close()

            elif self.stego == "Plain":
                key_file = open("secret/secretPlain_RSA_private.pem", "rb")
                self.private_key = key_file.read()
                key_file.close()

            self.private_key = RSA.importKey(self.private_key)
            self.private_key = PKCS1_OAEP.new(self.private_key)
            decrypted_string = self.private_key.decrypt(self.text.encode('latin-1'))

            print("Decrypted data is ", decrypted_string, len(decrypted_string),
                  type(decrypted_string))

            return decrypted_string.decode('latin-1')
