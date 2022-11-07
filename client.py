import socket
import json
import sys
import string

#Load the JSON file
file = sys.argv[1]
print(file)

user_data = open(file)
user_data = json.load(user_data)



name = user_data["id"]
if not isinstance(name, str) or len(name) == 0 or len(name) >= 64:
    print("Name must be a string shorter than 64 characters")
    sys.exit(1)

password = user_data["password"]
if not isinstance(password, str) or len(password) == 0 or len(password) >= 64:
    print("Password must be a string shorter than 128 characters")
    sys.exit(1)

steps = user_data["actions"]["steps"]
if not isinstance(steps, list) or len(steps) >= 64:
    print("Steps must be a list with less than 64 steps")
    sys.exit(1)

for step in steps:
    if not isinstance(step, str) or len(step) == 0:
        print("Step must be a string")
        sys.exit(1)
    if len(step) >= 64:
        print("Step string too big")
        sys.exit(1)
    if step.split()[0] not in ["INCREASE", "DECREASE"]:
        print("Step must start with INCREASE or DECREASE")
        sys.exit(1)
    if not step.split()[1].isdigit():
        print("Step value must be a number")
        sys.exit(1)

    if float(step.split()[1]) >= sys.maxsize:
        print("Number too big")
        sys.exit(1)

delay = user_data["actions"]["delay"]
if not isinstance(delay, int) or delay < 0:
    print("Delay must be an positive integer")
    sys.exit(1)

if delay >= 32767:
    print("Delay too big")
    sys.exit(1)

allow_list = set(string.ascii_letters + string.digits + ".-_")
if not all(letter in allow_list for letter in name):
    print("Only letters A-Z, digits 0-9 and _,.,- allowed for username!")
    sys.exit(1)
if not all(letter in allow_list for letter in password):
    print("Only letters A-Z, digits 0-9 and _,.,- allowed for password!")
    sys.exit(1)


# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_data = json.dumps(user_data)
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
