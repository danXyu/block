## Library Imports
from subprocess import call
from liblo import *
from pymongo import MongoClient
from datetime import datetime, date, time
import commands
import sys
import os
import time

## Database Connection
# client = MongoClient()
# db = client.block
# print(db)

## Constants
BUFFER_ZONE = 35

## Global Variables
counter = 0
l_forehead_map = {}
r_forehead_map = {}
l_forehead_mean = 0
r_forehead_mean = 0
l_possible = 0
r_possible = 0
completed = 0

## Script: Start
print "Starting Block Script"

## Function: clickLeft(l_forehead, r_forehead)
 # -------------------------------------------
def clickDirection(l_forehead, r_forehead):
    global BUFFER_ZONE, counter
    global l_forehead_map, r_forehead_map
    global l_forehead_mean, r_forehead_mean
    global r_possible, l_possible, completed
    counter += 1

    print(r_forehead_mean)
    print(r_forehead)
    print(r_possible)
    print(l_possible)
    print(completed)

    # When to skip.
    if (r_possible == 1 and r_forehead > r_forehead_mean + BUFFER_ZONE):
        return None
    elif (l_possible == 1 and r_forehead < r_forehead_mean - BUFFER_ZONE):
        return None

    # Compute whether or not to click left or right or none.
    if (r_forehead_mean - BUFFER_ZONE <= r_forehead <= r_forehead_mean + BUFFER_ZONE):
        completed = 0
        return None

    if (completed == 1):
        return None

    if (r_possible == 1 and r_forehead < r_forehead_mean - BUFFER_ZONE):
        print("Triggered Right!")
        r_possible = 0
        l_possible = 0
        completed = 1
        return 0
    elif (l_possible == 1 and r_forehead > r_forehead_mean + BUFFER_ZONE):
        print("Triggered Left!")
        r_possible = 0
        l_possible = 0
        completed = 1
        return 1

    print("Gets Here")
    if (r_forehead > r_forehead_mean + 0.3 * BUFFER_ZONE):
        l_possible = 0
        r_possible = 1
    if (r_forehead < r_forehead_mean - BUFFER_ZONE ):
        l_possible = 1
        r_possible = 0
    return None

## Muse Server: Start
class MuseServer(ServerThread):

    ## Method: __init__
     # ----------------
     # Starts the server and point it to listen to port 5001, which will be
     # where the Muse headset will be connected.
    def __init__(self):
        ServerThread.__init__(self, 5001)

    ## Method: '/muse/acc'
     # -------------------
     # Makes grabs the accelerometer data. For now, this is unused.
    # @make_method('/muse/acc', 'fff')
    # def acc_callback(self, path, args):
    #     acc_x, acc_y, acc_z = args
    #     print "%s %f %f %f" % (path, acc_x, acc_y, acc_z)

    ## Method: '/muse/eeg'
     # -------------------
     # Receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        global l_forehead_mean, r_forehead_mean, counter, db
        l_ear, l_forehead, r_forehead, r_ear = args

        # Keep track of the mean for right and left foreheads.
        if l_forehead_mean == 0: l_forehead_mean = l_forehead
        if r_forehead_mean == 0: r_forehead_mean = r_forehead

        # Insert all eeg data into mongo database with timestamps
        # db.eeg0.insert({
        #     "name": "Dan Yu",
        #     "time": datetime.now(),
        #     "eegval": l_ear
        # });
        # db.eeg1.insert({
        #     "name": "Dan Yu",
        #     "time": datetime.now(),
        #     "eegval": l_forehead
        # });
        # db.eeg2.insert({
        #     "name": "Dan Yu",
        #     "time": datetime.now(),
        #     "eegval": r_forehead
        # })
        # db.eeg3.insert({
        #     "name": "Dan Yu",
        #     "time": datetime.now(),
        #     "eegval": r_ear
        # });

        # Check the click direction to call device key presses.
        savedDirection = clickDirection(l_forehead, r_forehead)
        if (savedDirection == 1):
            os.system("monkeyrunner leftclick.py")
        if (savedDirection == 0):
            os.system("monkeyrunner rightclick.py")

        l_forehead_mean = ((l_forehead_mean * (counter - 1) + l_forehead) / counter)
        r_forehead_mean = ((r_forehead_mean * (counter - 1) + r_forehead) / counter)
        print "%s %f %f %f %f" % (path, l_ear, l_forehead, r_forehead, r_ear)

    ## Method: ''
     # ----------
     # Handle all extraneous methods.
    # @make_method(None, None)
    # def fallback(self, path, args, types, src):
    #     print "Unknown message \
    #     \n\t Source: '%s' \
    #     \n\t Address: '%s' \
    #     \n\t Types: '%s ' \
    #     \n\t Payload: '%s'" % (src.url, path, types, args)

## Error-Handling: Server Creation Failed
try: server = MuseServer()
except ServerError, err:
    print str(err)
    sys.exit()

## Server Process: Start
server.start()

## Program: Start
if __name__ == "__main__":
    while 1: time.sleep(1)