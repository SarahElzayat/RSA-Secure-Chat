'''
    Enctypted chat using RSA

'''

import math
import random
import Crypto.Util.number as cr

def generate_key_pair(keysize):
    '''
    Generating public/private key pair using RSA algorithm
    
    '''
    p = cr.getPrime(keysize//2)
    q = cr.getPrime(keysize//2)
    while q == p:
        q = cr.getPrime(keysize)

    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(1, phi - 1)  # public key
    while math.gcd(e, phi) != 1:
        e = random.randint(1, phi - 1)

    d = pow(e, -1, phi)  # private key

    return e, d, n


def alphabet_encryption(msg):
    '''
        Function for encrypting 5 chars of a message as specified in the document
    '''
    encrypted_message = 0

    for i, c in enumerate(msg):
        if 47 < ord(c) < 58:
            encrypted_message += int(c) * 37**i  # keep numbers from 0 - 9

        elif 96 < ord(c) < 123:  # map chars from a-z to 10-35
            encrypted_message += (ord(c) - 87) * 37**i

        else:
            encrypted_message += 36 * 37**i  # map space or any other special character to 36

    return encrypted_message


def alphabet_decryption(msg):
    '''
        Function for decrypting 5 chars of a message as specified in the document
    '''
    decrypted_message = ""
    while msg != 0:
        c = msg % 37
        if 0 <= c <= 9:
            decrypted_message += str(c)
        elif 10 <= c <= 35:
            decrypted_message += chr(c + 87)
        else:
            decrypted_message += " "
        msg //= 37
    return decrypted_message


def rsa_encryption(msg, pu_key, n):
    '''
    Function for encrypting a message using RSA
    msg is the plaintext after alphabet encryption
    '''
    return pow(msg, pu_key, n)


def rsa_decryption(msg, pr_key, n):
    '''
    Function for decrypting a message using RSA
    msg is the ciphertext
    '''
    return pow(msg, pr_key, n)


def sending_messages(c, pu_key, n):
    '''
    Function for sending messages
    Starts with sending the number of packets that will be sent
    Then encrypts the message in groups of 5 characters each as specified.
    '''
    while True:
        message = input("")
        c.send(str(math.ceil(len(message)/5)).encode())
        for i in range(0, len(message), 5):
            if i+5 < len(message):
                c.send(str(rsa_encryption(alphabet_encryption(
                    message[i:i+5]), pu_key, n)).encode())
            else:
                c.send(str(rsa_encryption(alphabet_encryption(
                    message[i:len(message)] + " "*(5 - (len(message) % 5))), pu_key, n)).encode())


def recieving_messages(c, pr_key, n):
    '''
    Function for recieving messages
    Starts by receiving the number of the packets, decrypts each and concatenates it
    to the final message string.
    '''
    while True:
        packets_number = int(c.recv(1024).decode())
        msg = ""
        for _ in range(packets_number):
            msg+= alphabet_decryption(rsa_decryption(int(c.recv(1024).decode()), pr_key, n))
        print("Sender: " + msg)
