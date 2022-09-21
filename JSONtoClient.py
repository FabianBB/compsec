import json
import logging
import time

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

# logging level configuration
logging.basicConfig(filename='logfile.log', level=logging.INFO)

# Function which carries out a list of given actions with delay seconds for a user with a given id
# Possible actions are increasing or decreasing a counter by an arbitrary amount
# Every action is recorded in a logfile with the id of the client and the counter's new value
def actionswithdelay(id, actions, delay):
    counter = 0
    for action in actions:
        print("Action", action ,"in progress.")
        tokens = action.split()
        if tokens[0] == 'INCREASE':
            counter = counter + int(tokens[1])
            logging.info('User ID {} increased by {}.'.format(id, tokens[1]))
        elif tokens[0] == 'DECREASE':
            counter = counter - int(tokens[1])
            logging.info('User ID {} decreased by {}.'.format(id, tokens[1]))
        print("Action", action,"completed.")
        time.sleep(delay)
    return counter

print("Counter at the end:", actionswithdelay(client.id, client.actions.steps, client.actions.delay))

