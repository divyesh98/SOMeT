import sys
import os
import random
import onetimepad

class OneTimePad():

    def __init__(self, string, stego):
        self.text = string
        self.key = ""
        self.all_characters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                               'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z',
                               'X', 'C', 'V', 'B', 'N', 'M', '0', '1', '2', '3',
                               '4', '5', '6', '7', '8', '9', 'q', 'w', 'e', 'r',
                               't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f',
                               'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b',
                               'n', 'm', '~', '@', '#', '$', '%', '^', '&', '*',
                               '(', ')', '_', '-', '+', '=', '[',']', '{', '}',
                               '\\', '|', ';', ':', '\'', '"', '<', '>', ',',
                               '.', '/', '?', ' ', ' ','\n']
        self.otp_length = 6
        self.all_char_len = len(self.all_characters)
        self.stego_type = stego

    def key_generator(self):

        k = ""
        num_characters = len(self.all_characters)
        for i in range(self.otp_length):
            k += random.choice(self.all_characters)

        if self.stego_type == "DCT":
            text_file = open("secret/secretDCTOTP.txt", "w")
            text_file.write(k)
            text_file.close

        elif self.stego_type == "Plain":
            text_file = open("secret/secretPlainOTP.txt", "w")
            text_file.write(k)
            text_file.close
        
        return k

    def encrypted_character(self, i, j):
        #i1 = self.all_characters.index(self.text[i])
        #i2 = self.all_characters.index(self.key[j])

        #new_index = (i1 ^ i2) % self.all_char_len

        character = chr(ord(self.text[i])^ord(self.key[j]))
        return character
        #return self.all_characters[new_index]
        
    def run(self, encrypt_decrypt):

        if encrypt_decrypt == "Encrypt":
            self.key = self.key_generator()

            encrypted_string = ""
            
            str_len = len(self.text)

            i = 0
            j = 0

            print("Key Generated is ", self.key)
            
            #while i < str_len - 1:
            #    if (i + self.otp_length) < str_len - 1:
            #        j = 0
            #       while j < self.otp_length:

            #            encrypted_string += self.encrypted_character(i, j)
            #            i += 1
            #            j += 1
            #    else:
            #        j = 0
            #        while i < str_len - 1:
                        
            #            encrypted_string += self.encrypted_character(i, j)
            #            i += 1

            encrypted_string = onetimepad.encrypt(self.text, self.key)
            
            print("Encrypted string is ", encrypted_string)    
            return encrypted_string
        else:

            if self.stego_type == "DCT":
                key_file = open("secret/secretDCTOTP.txt", "r")
                self.key = key_file.readline()
                key_file.close()

            elif self.stego_type == "Plain":
                key_file = open("secret/secretPlainOTP.txt", "r")
                self.key = key_file.readline()
                key_file.close()


            decrypted_string = ""
            
            str_len = len(self.text)

            i = 0
            j = 0

            #while i < str_len:
            #    if (i + self.otp_length) < str_len - 1:
            #        j = 0
            #        while j < self.otp_length:

            #            decrypted_string += self.encrypted_character(i, j)
            #           i += 1
            #            j += 1
            #    else:
            #        j = 0
            #        while i < str_len:
                        
            #            decrypted_string += self.encrypted_character(i, j)
            #            i += 1

            decrypted_string = onetimepad.decrypt(self.text, self.key)
            
            print("Hey ",decrypted_string)
            return decrypted_string
