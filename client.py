'''
    Client side of encrypted chat
'''
import socket
import threading
import utils


IP = '192.168.52.1'
PORT = 9999
KEYSIZE = 32

public_key, private_key, n_generated = utils.generate_key_pair(KEYSIZE)  # rsa.newkeys(KEYSIZE)
SERVER_PUBLIC_KEY = None
SERVER_N = None

print("Waiting for server to establish connection...")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
SERVER_PUBLIC_KEY = int(client.recv(KEYSIZE).decode())
SERVER_N = int(client.recv(1024).decode())
client.send(str(public_key).encode())
client.send(str(n_generated).encode())

print("Established connection")
print("Server public key is: ", SERVER_PUBLIC_KEY)
print("Server n is: ", SERVER_N)

threading.Thread(target=utils.sending_messages, args=(
    client, SERVER_PUBLIC_KEY, SERVER_N)).start()
threading.Thread(target=utils.recieving_messages, args=(
    client, private_key, n_generated)).start()
