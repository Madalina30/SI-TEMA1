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
        # raw = raw.decode()
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


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8005
print(port)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((socket.gethostname(), port))
iv = "0123456789abcdef"
k_prime = "6369706865722020"
global cbc_or_ecb
cbc_or_ecb = ""
message_from_b = ""


def xor_blocks(block_1, block_2):
    return format(int(block_1, 16) ^ int(block_2, 16), '032x')


def make_key():
    k = os.urandom(16)
    print(k)
    # encrypt the random key
    aes = AESCipher(k_prime, iv)
    encd = aes.encrypt(k)
    return encd


def encrypt_file(files, mode, key):
    cipher = AES.new(key, mode, iv)
    chunksize = 60 * 1024
    encrypted_text = b''
    with open(files, 'rb') as f:
        while True:
            file_string = f.read(chunksize)
            print(file_string)
            # multiple of 16
            if len(file_string) == 0:
                break
            elif len(file_string) % 16 != 0:
                file_string += b' ' * (16 - len(file_string) % 16)
            encrypted_text += cipher.encrypt(file_string)
        return encrypted_text


class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        global key
        global cbc_or_ecb
        while 1:
            msg_received = self.sock.recv(1024).decode()
            print('Client sent:', msg_received)
            print("socket:", self.sock.fileno())
            if msg_received == '':
            	print("exit")
            	break
            	# just exit if none of the clients is connected
            else:
            
            	if self.sock == clientsocket1:
            	    print("client socket 1")  # see if the message is either cbc or ecb and the server will send A the K
            	    if msg_received == "cbc":
            	        cbc_or_ecb = "cbc"
            	    elif msg_received == "ecb":
            	        cbc_or_ecb = "ecb"
            	    else:  # when the message is K or other
            	        cbc_or_ecb = ""
            	        pass
            	    if cbc_or_ecb != "":
            	        # sends K to A
            	        key = make_key()
            	        print(key)
            	        self.sock.send(key)
            	        clientsocket2.recv(1024).decode()
            	        clientsocket2.send(key)  # sends the key, but b needs to write something to take it
            	    else:
            	        self.sock.send(b"oiiiii")
            	    print(cbc_or_ecb)
            	elif self.sock == clientsocket2:
            	    print("client socket 2")
            	    if msg_received == 'give':
            	    	clientsocket2.send(cbc_or_ecb.encode('utf-8'))
            	    elif msg_received == "done":  # i se trimite lui B continutul unui fisier criptat pe blocuri
            	        # pe care acesta il decripteaza prin modul selectat - inceputul mesajului primit cbc_or_ecb
            	        # mai intai se vede ce a fost ales
            	        aes = AESCipher(k_prime, iv)
            	        k_decrypted = aes.decrypt(key)
            	        if cbc_or_ecb == "cbc":
            	            mode = AES.MODE_CBC
            	            text_encrypted = encrypt_file("f.txt", mode, k_decrypted)
            	            print("encr", text_encrypted)
            	            clientsocket2.send(text_encrypted)
            	            print("cbc")
            	        else:
            	            mode = AES.MODE_ECB
            	            text_encrypted = encrypt_file("f.txt", mode, k_decrypted)
            	            print("encr", text_encrypted)
            	            # print(k_decrypted)
            	            clientsocket2.send(text_encrypted)
            	            print("ecb")
            	    else:
            	        self.sock.send(b"oiiiii")
            	# TODO: exit
            	# TODO: CBC/ECB ALEGE SI TRIMITE CATRE B

serversocket.listen(5)
print('server started and listening')
clientsocket1, address1 = serversocket.accept()
clientsocket2, address2 = serversocket.accept()
# while 1:
client(clientsocket1, address1)
client(clientsocket2, address2)
