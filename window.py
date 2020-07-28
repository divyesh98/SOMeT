import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import cv2
from PIL import Image, ImageTk
from stegano import lsb,lsbset,red, steganalysis
from stegano.lsbset import generators
import inspect
from DCT import DCT
# import ScrollableFrame as sf
import ntpath

from LSBSteg import LSBSteg
from OneTimePad import OneTimePad
import os
from AESCipher import AESCipher
from DESCipher import DESCipher
from RSACipher import RSACipher

import matplotlib.pyplot as plt
import numpy as np
import csv
import math

from ButtonDefinitions import analyse_mse, analyse_psnr, mse, psnr, compare_images, analyse_strings

    
container2wt = 0



def path_leaf(path):	
    head, tail = ntpaht.split(path)
    return tail or ntpath.basename(head)

def get_file_name(img_path):
    return os.path.basename(img_path)
#https://www.hlevkin.com/06testimages.htm
def exit_app():
    print('Exit App')
    messagebox = tk.messagebox.askyesno("Exit Application","Are you sure you want to exit?")
    print(messagebox)
    if (messagebox):
        root.quit()

def select_image():
    print('Select Image')
    global image_path
    image_path = tk.filedialog.askopenfilename(title="Select image", filetypes=[("all files", '*.*')])
    print(image_path)
    if (image_path):
        root.update_idletasks()
        global original_image_label
        load = Image.open(image_path)
        original_image = ImageTk.PhotoImage(load)
        print(type(original_image))
        original_image_label.config(image = original_image)
        original_image_label.image = original_image
        original_image_label.pack(in_=container2, fill=tk.BOTH, expand=True)

def displayImage(path):
    print(type(path))
    # im = Image.fromarray(image)
    global processed_image_label
    # processed_image = ImageTk.PhotoImage(image=im)
    # print(type(processed_image))
    load = Image.open(path)
    processed_image = ImageTk.PhotoImage(load)
    processed_image_label.config(image=processed_image)
    processed_image_label.image = processed_image
    processed_image_label.pack(in_=container4, fill=tk.BOTH, expand=True)

def displaySecret(secret):
    clear_processed_image()
    global processed_image_label
    processed_image_label.config(text=secret)
    # processed_image_label.image = processed_image
    processed_image_label.pack(in_=container4, fill=tk.BOTH, expand=True)

def clear_image():
    print('Save Image')
    # print(processed_image_label.image)
    clear_processed_image()


def saveImage():
    print("af")

def saveSecretToFile(secret):
    print("saveSecretToFile")
    f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    text2save = str(secret)
    f.write(text2save)
    f.close()

def clear_processed_image():
    print("clear image")
    processed_image_label.config(image='')
    processed_image_label.pack(in_=container4, fill=tk.BOTH, expand=True)

def clear_text_description():
    print("clear image")
    text2.delete('1.0', tk.END)

# Enter data from secret file into text1
def select_secret_file():
    # global secret_image_path
    print("Select secret file")
    secret_file = tk.filedialog.askopenfile(title="Select file", filetypes=[("All files", '*.*')])
    # print(secret_image_path)
    data = secret_file.read()
    text1.insert(tk.END, data)


def process():
    try:
        print('process()')
        encrypt_decrypt = options_clicked.get()
        algo_technique = technique_options_clicked.get()
        encryption_technique = encryption_options_clicked.get()
        
        # Check for secret data
        secret_string = text1.get("1.0",tk.END)

        # check for carrier
        try: image_path
        except NameError:
            tk.messagebox.showwarning("Data Required","Please select carrier image to proceed")
            return
        # original_image = cv2.imread(image_path)
        print(secret_string)
        if (algo_technique == technique_options[0]):
            # LSB Algorithm
            lsbAlgoDefault(encrypt_decrypt, secret_string, encryption_technique)
        elif (algo_technique == technique_options[1]):
            # stegano plain
            lsbAlgoStegano("DCT", secret_string, encrypt_decrypt, encryption_technique)
    except NameError as error:
        print(error)

def is_grey_scale(image_path):
    img = Image.open(image_path).convert('RGB')
    img1 = img
    w,h = img1.size
    for i in range(w):
        for j in range(h):
            r,g,b = img1.getpixel((i,j))
            if r != g != b:
                return False
    return True        

def compare_strings(original, derived):
    if len(original) != len(derived):
        return 0.0

    else:
        count = 0
        for i in range(len(original)):
            if original[i] == derived[i]:
                count += 1

        return float(count/len(original))


def addtofile(stego_type, enc_type, percentage):
    flag = 0
    print("Add to file")
    with open("secret/StringAnalysis.csv", 'r+') as varfile:
        read_object = csv.reader(varfile)
        titles = next(read_object)
        print("1")

        for row in read_object:
            print("2")
            if len(row) > 0:
                print(row)
                print(stego_type, enc_type)
                if row[0] == stego_type and row[1] == enc_type:
                    print("Entered")
                    if len(row) > 2:
                        row[2] = ((float(row[2]) + percentage)/2)
                        flag = 1

        if flag == 0:
            write_object = csv.writer(varfile)
            write_object.writerow([stego_type, enc_type, percentage])


def lsbAlgoStegano(type, secret_string, encrypt_decrypt, encryption_technique):
    if (encrypt_decrypt == options[0]):
        if (len(secret_string) == 1):
            print("Empty Secret:: Showing warning")
            tk.messagebox.showwarning("Data Required", "Please enter secret data to be encoded")
            return
    if (type == "DCT"):
        if (encrypt_decrypt == options[0]):
            file_name = encryption_technique + "DCT.txt"
            text_file = open(file_name, "w")
            text_file.write(str(secret_string))
            text_file.close
            if encryption_technique == "OTP":
                enc = OneTimePad(secret_string, "DCT")
                enc_string = enc.run(encrypt_decrypt)

            elif encryption_technique == "RSA":
                enc = RSACipher(secret_string, "DCT")
                enc_string = enc.run(encrypt_decrypt)

            elif encryption_technique == "AES":
                enc = AESCipher(secret_string, "DCT")
                enc_string = enc.run(encrypt_decrypt)

            elif encryption_technique == "DES":
                enc = DESCipher(secret_string, "DCT")
                enc_string = enc.run(encrypt_decrypt)
                
            outFile = "secret/secretDCT.png"
            x = DCT(image_path)
            secret = x.DCTEn(enc_string, outFile)
            print("secret :: DCT:: ",secret)
            # secret = red.hide(image_path, secret_string)
            # secret.save("secret.png")
            displayImage("secret/secretDCT.png")
            img1 = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            print(img1.shape)
            img2 = cv2.imread("secret/secretDCT.png", cv2.IMREAD_UNCHANGED)
            print(img1.shape, img2.shape)
            if is_grey_scale(image_path) and len(img2.shape) == 3:
                imgA = cv2.cvtColor(img1, cv2.COLOR_BGRA2GRAY)
                imgB = cv2.cvtColor(img2, cv2.COLOR_BGRA2GRAY)
            else:
                imgA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                imgB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            compare_images(imgA, imgB, "DCT", encryption_technique)
        else:
            y = DCT(image_path)
            secret = y.DCTDe()
            # secret = red.reveal(image_path)
            print("Secret is ", secret)
            if encryption_technique == "OTP":
                dec = OneTimePad(secret, "DCT")
                secret_message = dec.run(encrypt_decrypt)

            elif encryption_technique == "RSA":
                dec = RSACipher(secret, "DCT")
                secret_message = dec.run(encrypt_decrypt)

            elif encryption_technique == "AES":
                dec = AESCipher(secret, "DCT")
                secret_message = dec.run(encrypt_decrypt)

            elif encryption_technique == "DES":
                dec = DESCipher(secret, "DCT")
                secret_message = dec.run(encrypt_decrypt)

            #dec = OneTimePad(secret, "DCT")
            #secret_message = dec.run(encrypt_decrypt)
            filename = encryption_technique + "DCT.txt"
            key_file = open(filename, "r")
            original_message = key_file.readline()
            key_file.close()
            precentage_comparison = compare_strings(original_message, secret_message)
            print("The strings are equal by", precentage_comparison,"parts")
            addtofile("DCT", encryption_technique[:3], precentage_comparison)
            displaySecret(secret_message)
            saveSecretToFile(secret_message)



def lsbAlgoDefault(encrypt_decrypt, secret_string, encryption_technique):
    # if (algo_technique == technique_options[0]):
        # LSB:: Text Steganography
        if (encrypt_decrypt == options[0]):
            print("LSB:::Text::: Encrypt")
            # Warning for secret string
            if (len(secret_string) == 1):
                print("Empty Secret:: Showing warning")
                tk.messagebox.showwarning("Data Required", "Please enter secret data to be encoded")
                return
            # encoding
            steg = LSBSteg(cv2.imread(image_path))
            file_name = encryption_technique + "Plain.txt"
            text_file = open(file_name, "w")
            text_file.write(str(secret_string))
            text_file.close()
            if encryption_technique == "OTP":
                enc = OneTimePad(secret_string, "Plain")
                enc_string = enc.run(encrypt_decrypt)

            elif encryption_technique == "RSA":
                enc = RSACipher(secret_string, "Plain")
                enc_string = enc.run(encrypt_decrypt)

            elif encryption_technique == "AES":
                enc = AESCipher(secret_string, "Plain")
                enc_string = enc.run(encrypt_decrypt)

            elif encryption_technique == "DES":
                enc = DESCipher(secret_string, "Plain")
                enc_string = enc.run(encrypt_decrypt)
                
            img_encoded = steg.encode_text(enc_string)
            cv2.imwrite("secret/secret.png", img_encoded)
            displayImage("secret/secret.png")
            img1 = cv2.imread(image_path)
            img2 = cv2.imread("secret/secret.png")
            imgA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            imgB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            compare_images(imgA, imgB, "LSB", encryption_technique)
        else:
            print("LSB:::Text::: Decrypt")
            # decoding
            print(image_path)
            im = cv2.imread(image_path)
            steg = LSBSteg(im)
            secret = steg.decode_text()

            print("Secret is", secret)
            
            if encryption_technique == "OTP":
                dec = OneTimePad(secret, "Plain")
                secret_message = dec.run(encrypt_decrypt)

            elif encryption_technique == "RSA":
                dec = RSACipher(secret, "Plain")
                secret_message = dec.run(encrypt_decrypt)

            elif encryption_technique == "AES":
                dec = AESCipher(secret, "Plain")
                secret_message = dec.run(encrypt_decrypt)

            elif encryption_technique == "DES":
                dec = DESCipher(secret, "Plain")
                secret_message = dec.run(encrypt_decrypt)

            
            filename = encryption_technique + "Plain.txt"
            key_file = open(filename, "r")
            original_message = key_file.readline()
            key_file.close()
            precentage_comparison = compare_strings(original_message, secret_message)
            print("The strings are equal by", precentage_comparison,"parts")
            addtofile("LSB", encryption_technique[:3], precentage_comparison)
            #dec = OneTimePad(secret, "Plain")
            #secret_message = dec.run(encrypt_decrypt)
            displaySecret(secret_message)
            print("Text value:", secret_message)


def technique_callback(*args):
    clear_text_description()
    all_generators = inspect.getmembers(generators, inspect.isfunction)
    option = technique_options_clicked.get()
    print("technique_callback: ", option)
    data = ""
    if (option == technique_options[0]):
        data ="Technique 1\nLSB is the lowest bit in a series of numbers in binary. e.g. in the binary number: 10110001, the least significant bit is far right 1.\n" \
              "The LSB  based Steganographyis one of the steganographic methods,  used  to  embed  the  secret  data  in  to  the  least significant bits of the " \
              "pixel values in a cover image. e.g. 240 can be hidden in the first eight bytes of three pixels in a 24 bit image."
    elif (option == technique_options[1]):
        data = "DCT   coefficients   are   used   for   JPEG   compression.   It separates  the  image  into  parts  of  differing  importance.  " \
               "It transforms a signal or image from the spatial domain to the frequency  domain.  It  can  separate  the  image  into  high, middle and low frequency " \
               "components. \n" \
               "Signal  energy  lies  at  low  frequency  in  image;  it  appears  in the  upper  left  corner  of  the  DCT.  Compression  can  be achieved   since   " \
               "the   lower   right   values   represent   higher frequencies,  and  generally  small  enough  to  be  neglected with little visible distortion. " \
               "DCT is used in steganography as- \n  1. Image is broken into 8×8 blocks of pixels. \n  2. Working from left to right, top to bottom, the DCT is applied to each block." \
               " \n  3. Each  " \
               "block  is  compressed  through  quantization table  to  scale  the  DCT  coefficients  and  message  is embedded in DCT coefficients."
    text2.insert(tk.END, data)
    print(data)

root = tk.Tk()
root.geometry("600x400")
root.title("Image Cryptography and Steganography")

top = tk.Frame(root, borderwidth=1,relief="solid")
top1 = tk.Frame(root, borderwidth=1,relief="solid")
bottom1 = tk.Frame(root, borderwidth=1, relief="solid")
bottom = tk.Frame(root, borderwidth=1,relief="solid")
left = tk.Frame(root, borderwidth=1, relief="solid")
right = tk.Frame(root, borderwidth=1, relief="solid")
container1 = tk.Frame(left, borderwidth=1, relief="solid")
container2 = tk.Frame(left, borderwidth=1, relief="solid")
container3 = tk.Frame(right, borderwidth=1, relief="solid")
container4 = tk.Frame(right, borderwidth=1, relief="solid")

secret_label = tk.Label(container1, text="Enter secret")
# original_img_label = tk.Label(container2, text="Original Image")
description_label = tk.Label(container3, text="Description")
# processed_img_label = tk.Label(container4, text="Processed Image")

top.pack(side="top", expand=False, fill="both")
top1.pack(side="top", expand=False, fill="both")
bottom1.pack(side="bottom", expand=False, fill="both")
bottom.pack(side="bottom", expand=False, fill="both")
left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
container1.pack(expand=False, fill="both", padx=5, pady=5)
container2.pack(expand=False, fill="both", padx=5, pady=5)
container3.pack(expand=False, fill="both", padx=5, pady=5)
container4.pack(expand=False, fill="both", padx=5, pady=5)

container2wt = container2.winfo_width()
#print(container2wt)
original_image_label = tk.Label(root, width=container2wt)
processed_image_label = tk.Label(root, width=container2wt)

secret_label.pack()
# original_img_label.pack()
description_label.pack()
# processed_img_label.pack()


# Buttons
select_img_btn = tk.Button(root,text='Select Image', width=35, command=select_image)
select_img_btn.pack(in_=top, side="left")

select_secret_img_btn = tk.Button(root,text='Select secret file', width=35, command=select_secret_file)
select_secret_img_btn.pack(in_=top1, side="left")

clear_btn = tk.Button(root,text='Clear Image', width=35, command=clear_image)
clear_btn.pack(in_=bottom, side="left")

exit_btn = tk.Button(root,text='Exit App', width=35, command=exit_app)
exit_btn.pack(in_=bottom, side="right")

process_btn = tk.Button(root,text='Process', width=35, command=process)
process_btn.pack(in_=top, side="right")

# Drop down menu
options = [
    "Encrypt",
    "Decrypt"
]
technique_options = [
    "LSB Algorithm - Plain",
    "Discrete Cosine Transform"
]

encryption_options = [
    "OTP",
    "RSA",
    "AES",
    "DES"
]

options_clicked = tk.StringVar()
options_clicked.set(options[0])
technique_options_clicked = tk.StringVar()
technique_options_clicked.trace("w",technique_callback)
technique_options_clicked.set(technique_options[0])
encryption_options_clicked = tk.StringVar()
encryption_options_clicked.set(encryption_options[0])

image_name = ""

drop = tk.OptionMenu(root, options_clicked, *options)
drop.pack(in_=top, anchor="n", side="bottom")
encryption_drop = tk.OptionMenu(root, encryption_options_clicked, *encryption_options)
encryption_drop.pack(in_=top1, anchor="n", side="left")
technique_drop = tk.OptionMenu(root, technique_options_clicked, *technique_options)
technique_drop.pack(in_=top1, anchor="n", side="bottom")

# textbox and scrollbar
text1 = tk.Text(root, width=35, height=5)
text2 = tk.Text(root, width=35, height=5)
scrollbar1 = tk.Scrollbar(root)
scrollbar2 = tk.Scrollbar(root)
scrollbar1.config(command=text1.yview)
scrollbar2.config(command=text2.yview)
text1.config(yscrollcommand=scrollbar1.set)
text2.config(yscrollcommand=scrollbar2.set)
scrollbar1.pack(in_=container1, side=tk.RIGHT, fill=tk.Y)
scrollbar2.pack(in_=container3, side=tk.RIGHT, fill=tk.Y)
text1.pack(in_=container1, side=tk.LEFT, fill=tk.BOTH, expand=True)
text2.pack(in_=container3, side=tk.LEFT, fill=tk.BOTH, expand=True)

#Analysing Buttons
analyse_mse_btn = tk.Button(root, text = "Analyse MSE", width = 35, command = analyse_mse)
analyse_mse_btn.pack(in_ = bottom1, side = "left")

analyse_psnr_btn = tk.Button(root, text = "Analyse PSNR", width = 35, command = analyse_psnr)
analyse_psnr_btn.pack(in_ = bottom1, side = "right")

analyse_strings = tk.Button(root, text = "Analyse Strings", width = 35, command = analyse_strings)
analyse_strings.pack(in_ = bottom1, side = "bottom")


all_generators = inspect.getmembers(generators, inspect.isfunction)
#for generator in all_generators:
#    print(generator[0], generator[1].__doc__)

root.mainloop()
