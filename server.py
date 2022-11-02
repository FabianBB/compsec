import json
import socket
import threading
import hashlib
import time

# Create Socket (TCP) Connection
ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting...')
ServerSocket.listen(5)
HashTable = {}
HashTable_count = {}


def threaded_client(connection):
    # Receive json
    jsonReceived = connection.recv(1024)
    data = jsonReceived.decode('utf-8')
    data = json.loads(data)
    print("Json received -->", data)

    # Save elements of json

    name = data["id"]

    password = data["password"]

    steps = data["actions"]["steps"]

    delay = data["actions"]["delay"]

    password = password

    name = name

    password = hashlib.sha256(str.encode(password)).hexdigest()  # Password hash using SHA256

    # Registration phase
    if name not in HashTable:
        HashTable[name] = password
        HashTable_count[name] = 0
        connection.send(str.encode('Registration Successful'))
        print('Registered : ', name)
        print("{:<8} {:<20}".format('USER', 'PASSWORD'))
        for k, v in HashTable.items():
            label, num = k, v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")
        counter_phase(name, steps, delay)
    else:
        # If already existing user, check if the entered password is correct
        if (HashTable[name] == password):
            # read from log file
            with open("log.txt", 'r') as log:
                loglines = log.read().split("\n")
            log.close()
            # find line with last transaction of a given user and extract the counter
            s = name + ","
            indices = [s in line for line in loglines]
            idx = max([i for i, x in enumerate(indices) if x])
            HashTable_count[name] = int(loglines[idx].split(",")[1])
            connection.send(str.encode('Connection Successful'))  # Response Code for Connected Client
            print('Connected : ', name)
            print("-------------------------------------------")
            counter_phase(name, steps, delay)
        else:
            connection.send(str.encode('Login Failed'))  # Response code for login failed
            print('Connection denied : ', name)
    connection.close()


# Handles the counter
def counter_phase(name, steps, delay):
    for step in steps:
        string = step.split()
        if string[0] == "INCREASE":
            HashTable_count[name] = HashTable_count[name] + float(string[1])
        if string[0] == "DECREASE":
            HashTable_count[name] = HashTable_count[name] - float(string[1])
        log = open("log.txt", "a+")
        log.write(name + "," + str(HashTable_count[name]) + "\n")
        log.close()
        print("Counter: ", name, HashTable_count[name])
        time.sleep(delay)
    HashTable_count[name] = 0  # Reset counter


while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)
    )
    client_handler.start()
    ThreadCount += 1
ServerSocket.close()
