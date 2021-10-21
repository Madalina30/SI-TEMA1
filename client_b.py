# gets ecb/cbc
# gets from A the K random + decrypts the key + sends back to A a message
# if message received by A, A sends to B a file encrypted and B decrypts it and prints the message

import socket
import socket
from threading import *
import os
from M2Crypto import EVP
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher:

    def __init__(self, key, ivv):
        self.bs = 16
        self.iv = ivv
        self.key = key

    def encrypt(self, raw):
        #raw = raw.decode()
        cipher = AES.new(self.key, AES.MODE_OFB, self.iv)
        return cipher.encrypt(raw)

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_OFB, self.iv)
        return cipher.decrypt(enc)

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8005
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((socket.gethostname(), port))
iv = "0123456789abcdef"
k_prime = "6369706865722020"
k_decrypted = ""
# decrypt key
# decrypt file

def decrypt_string(string, mode, key):
	cipher = AES.new(key, mode, iv)
	decrypted_text = b''
	while True:
            file_string = string[0:16]
            string = string[16:]
            if len(file_string) == 0:
                break
            elif len(file_string) % 16 != 0:
                file_string += ' ' * (16 - len(file_string) % 16)
            decrypted_text += cipher.decrypt(file_string)
	return decrypted_text

cbc_or_ecb = ''

def ts(string):
	# when B asks for the key, he gets it and decrypts it
	# sends to A a message that he is ready
	# gets from A an encrypted file and prints it
    global k_decrypted
    global cbc_or_ecb
    s.send(string.encode())
    data = ''
    data = s.recv(1024)
    if len(data) < 20 and '\\' in str(data):
    	print('got:', data)
    	new_data = data
    	aes = AESCipher(k_prime, iv)
    	k_decrypted = aes.decrypt(new_data)
    	print('decrypted:',k_decrypted)
    elif 'cbc' in str(data) or 'ecb' in str(data):  # decode with cbc the data without first 4
    	cbc_or_ecb = data.decode()
    	print(cbc_or_ecb)
    else:
    	print(data)
    	pass
    if cbc_or_ecb == 'cbc' and len(data) > 20:
    	mode = AES.MODE_CBC
    	print('string given', data)
    	decrypted_text = decrypt_string(data, mode, k_decrypted)
    	#print('ceva aici', data)
    	print('This is the file\'s content:', decrypted_text.decode())
    elif cbc_or_ecb == 'ecb' and len(data) > 20:
    	mode = AES.MODE_ECB
    	print('string given', data)
    	decrypted_text = decrypt_string(data, mode, k_decrypted)
    	#print('ceva aici', data)
    	print('This is the file\'s content:', decrypted_text.decode())


while 2:
    try:
    	r = input('enter: ')
    	if r == 'exit':  # sa se inchida conexiunea cu serverul, dar sa se inchida si pt server si celalalt client?
    		print("exiting")
    		break
    	ts(r)
    except KeyboardInterrupt:
    	print("\nExiting")
    	break

s.close()
