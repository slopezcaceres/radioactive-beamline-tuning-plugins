from requests import get
import numpy as np

# Get the set field value and initially requested current from the controls system
# For the get(BASE_URL, json=data) function below to work, you need to take the following actions:
#
# ACTION 1 
# Ask the ATLAS operator to enable AWACS.
#
# ACTION 2
# Open a terminal and type:
#   ssh -v -L 5000:146.139.66.20:8042 -N ANLusername@acslogin.phy.anl.gov
#
# Replace ANLusername with your username, enter your password. Leave the terminal open.
# For less details, remove the "–v" option from the ssh command above.
# For quite mode, replace –v with –q.
# When using the –v option, the following lines indicate a successful execution: 
#   Authenticated to acslogin.phy.anl.gov ([146.139.228.11]:22) using "keyboard-interactive". 
#   debug1: Local connections to LOCALHOST:5000 forwarded to remote address 146.139.66.20:8042
#
# The –L option won't create an interactive session in the first terminal. That is OK.
# Port 5000 could be changed to other port numbers. However port 8042 and the IP address
# for ACS020 are fixed.

BASE_URL = "http://127.0.0.1:5000/"

# K0 controls
awacsControls = [{"device":"STK000","chan":"CONTROL_X"},  
                 {"device":"STK000","chan":"CONTROL_Y"},
                 {"device":"LAUREL_RATEMETER","chan":"READ"},]

awacsControlsReply = get(BASE_URL, json=awacsControls)
awacsControlsJSON = awacsControlsReply.json()
print(awacsControlsJSON)


device = awacsControlsJSON['data']
array_length = len(device)
val = np.zeros(array_length, dtype=float)
for index in range(0, array_length):
    val[index] = device[index]['val']
# An array with just numbers.
print(val)