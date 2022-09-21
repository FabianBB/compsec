import socket
import os
import threading
import hashlib

# Create Socket (TCP) Connection
ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)
HashTable = {}
HashTable_count = {}


# Function : For each client
def threaded_client(connection):
    connection.send(str.encode('ENTER USERNAME : '))  # Request Username
    name = connection.recv(2048)
    connection.send(str.encode('ENTER PASSWORD : '))  # Request Password
    password = connection.recv(2048)
    password = password.decode()
    name = name.decode()
    password = hashlib.sha256(str.encode(password)).hexdigest()  # Password hash using SHA256
    # REGISTERATION PHASE
    # If new user,  regiter in Hashtable Dictionary
    if name not in HashTable:
        HashTable[name] = password
        HashTable_count[name] = 0
        connection.send(str.encode('Registeration Successful'))
        print('Registered : ', name)
        print("{:<8} {:<20}".format('USER', 'PASSWORD'))
        for k, v in HashTable.items():
            label, num = k, v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")
        connection.send(str.encode('INCREASE / DECREASE (I/D) : '))
        count = connection.recv(2048)
        count = count.decode()
        if count == "I":
            HashTable_count[name] = HashTable_count[name] + 1
        if count == "D":
            HashTable_count[name] = HashTable_count[name] - 1
        print(HashTable_count[name])

    else:
        # If already existing user, check if the entered password is correct
        if (HashTable[name] == password):
            connection.send(str.encode('Connection Successful'))  # Response Code for Connected Client
            print('Connected : ', name)
            print("-------------------------------------------")
            connection.send(str.encode('INCREASE / DECREASE (I/D) : '))
            count = connection.recv(2048)
            count = count.decode()
            if count == "I":
                HashTable_count[name] = HashTable_count[name] + 1
            if count == "D":
                HashTable_count[name] = HashTable_count[name] - 1
            print(HashTable_count[name])

        else:
            connection.send(str.encode('Login Failed'))  # Response code for login failed
            print('Connection denied : ', name)
    # while received message is not exit keep receiving messages
    while True:
        data = connection.recv(2048)
        reply = 'Server Output : ' + data.decode()
        if not data:
            break
        connection.sendall(str.encode(reply))

    connection.close()


while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)
    )
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))
#ServerSocket.close()