import os
import numpy as np

# read from logfile line by line
with open("log.txt") as log:
    loglines = log.read().split("\n")

print(loglines)
# find indices of lines that contain the username and get the maximum index
# s = HashTable[name] + ","
#indices = [s in line for line in loglines]
#idx = max([i for i, x in enumerate(indices) if x])

# extract the counter value from the last logged transaction of a user
#HashTable_count[name] = loglines[idx].split(",")[1]

