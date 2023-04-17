'''
    Server side of encrypted chat
'''
import socket
import threading
import utils

IP = '192.168.52.1'
PORT = 9999
KEYSIZE = 32

public_key, private_key, n_generated = utils.generate_key_pair(KEYSIZE)  # rsa.newkeys(KEYSIZE)
CLIENT_PUBLIC_KEY = None
CLIENT_N = None

print("Waiting for client to establish connection...")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
client, _ = server.accept()
client.send(str(public_key).encode())
client.send(str(n_generated).encode())
CLIENT_PUBLIC_KEY = int(client.recv(KEYSIZE).decode())
CLIENT_N = int(client.recv(1024).decode())

print("Established connection")
print("Client public key is: ", CLIENT_PUBLIC_KEY )
print("Client n is: ", CLIENT_N )

threading.Thread(target=utils.sending_messages, args=(client, CLIENT_PUBLIC_KEY, CLIENT_N)).start()
threading.Thread(target=utils.recieving_messages, args=(client, private_key, n_generated)).start()
