import socket
from threading import *
import os
from M2Crypto import EVP
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

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


def ts(string):
    s.send(string.encode())
    data = ''
    data = s.recv(1024)
    if '\\' in str(data):
    	print('got:', data)
    	new_data = data
    	aes = AESCipher(k_prime, iv)
    	k_decrypted = aes.decrypt(new_data)
    	print('decrypted:', k_decrypted)
    else:
    	print(data.decode())
    	
    # it needs to send a file to b after getting a message back


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

