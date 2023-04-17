# Encrypted chat using RSA algorithm

![](https://github.com/SarahElzayat/RSA-Secure-Chat/blob/master/logo.png)

##### Python version

Python 3.11.1

##### Packages to install

```
pip install cryptodome
pip install socket
pip install threading 
pip install matplotlib
```

##### How to run chat

Start by running server first then client

```
python ./server.py
python ./client.py
```

##### How it works

The RSA algorithm is used to encrypt and decrypt messages between the server and the client. When the client connects to the server, it sends its public key to the server. The server uses this public key to encrypt messages that it sends to the client. The client uses its private key to decrypt these messages. Similarly, when the client sends a message to the server, it encrypts the message using the server's public key, and the server decrypts the message using its private key.

##### How to run attacks

Run all cells in the attacks.ipynb file

##### How to run encryption/decryption time analysis

Run all cells in the encrypting_decrypting_analysis.ipynb file
