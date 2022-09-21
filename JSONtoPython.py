import json

class Client:

    # constructor
    def __init__(self, json_data):
        self.__dict__.update(json_data)

# turns python dictionary into an object
def dict2obj(json_data):
    return json.loads(json.dumps(json_data), object_hook=Client)

# open and load data from JSON file
with open('config.JSON') as config_file:
    json_data = json.load(config_file)

# turn the data from the JSON file into a client object
client = dict2obj(json_data)

print("User ID: ", client.id)
print("User password: ", client.password)
print("IP: ", client.server.ip)
print("Port: ", client.server.port)
print("Action delay in seconds: ", client.actions.delay)
print("Client actions: ", client.actions.steps)
