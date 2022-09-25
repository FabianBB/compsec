# compsec
To run this, just open up n terminal windows and run the following commands in each:
```
python3 server.py
python3 client.py <filename.JSON>
```
repeat "python3 client.py" for as many clients as you want.

## What is this?
If you want to change the behaviour of the client (e.g. change the delay or the steps of the counter) simply modify the 
json file (config.JSON) before running client.py. 

## How does it work? 
The client sends a single json file to the server with its data and the information of the actions that it wants to 
perform. The server receives the json file and after confirming the registration of the user or the log-in, it starts 
executing the actions with the specified delay. 