import socket
import json
import sys

#Load the JSON file
file = sys.argv[1]
print(file)

user_data = open(file)
user_data = json.load(user_data)
user_data = json.dumps(user_data)

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
try:
    client.connect(('127.0.0.1', 1233))
    # Send json
    client.send(user_data.encode())
    # Receive response
    response = client.recv(2048)
    response = response.decode()
    print(response)

except socket.gaierror:
    print('There was an error resolving the host')
    sys.exit()

client.close()