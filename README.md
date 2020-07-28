# SOMeT
Secure Online Message Transmission

As the name suggests, this is a technique used for secure online message transmission over internet.

First, the message to be sent, taken in text format, is encrypted using one of the four Cryptographic Technique, i.e. RSA, AES, DES or OTP. Then this encrypted message is embeded in an image using one of the two Steganographic Technique, i.e. LSB and DCT.

The image obtained can be then sent over internet for hidden transfer of message and can be decoded on the other side, provided it knows the Cryptographic and Steganographic technique used.

A comparative study is also performed for the given algorithms by comparing use of various cryptographic technique with the steganographoc technique. The results can be found in the secret folder.


To get more insight on work done, one can go through the pdf report uploaded.




Run the Code:

Run the window.py file

This opens up a GUI. Choose the Cryptographic and Steganogrpahic technique you want to use to hide the message. Write the message in text-box or upload a text file containing message and then click the process button to get encoded image.

To see the analysis of the algorithms, use analyse_stego and analyse_string buttons.
