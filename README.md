# Joycontrol-udp-server

A simple UDP server script for joycontrol (https://github.com/mart1nro/joycontrol)

I made this script so I and others (using parsec) can play on my switch


# Setup

* install joycontrol (https://github.com/mart1nro/joycontrol/blob/master/README.md)

  * `git clone https://github.com/mart1nro/joycontrol.git`

  * `cd joycontrol`

  * `sudo pip3 install .`
  
* Optional Steps

  * Set the environment var "jcs_host" to your local IPv4 otherwise "0.0.0.0" is used
  * Set the environment var "jcs_port" to your preffered port otherwise "7777" is used
  
* install additional dependencies

  * `sudo pip3 install asyncio asyncio_dgram`

# Usage

* without BT MAC ADDRESS

  * on your Switch go to the "Change Grip/Order" Page

  * `sudo python3 server.py PRO_CONTROLLER`

* with BT MAC ADDRESS

  * `sudo python3 server.py -r [YOUR SWITCH BLUETOOTH MAC ADDRESS] PRO_CONTROLLER`

* run the client application (not included in this repo yet)

#Known Issues

* Server will crash if the Switch force disconnects the emulated controller

  * temporary fix: restart the server

# How to get the BT MAC ADDRESS

- Run joycontrol

- Open new terminal

- `bluetoothctl devices`

#  The Protocol (for custom client applications)

the server expects udp packets encoded in UTF-8 with the following format. Keep in mind the controller will only update when a new packet is recieved so make sure to send enough packets per second (personally I send packets with a delay of 20ms (50hz))

ls[direction] rs[direction] [space seperated buttons]

* [direction] (both analog sticks)

  * 0: neutral position
  * 1: up
  * 2: up right
  * 3: right
  * 4: right down
  * 5: down
  * 6: down left
  * 7: left
  * 8: left up
  
* [space seperated buttons]

  * "a": A
  * "b": B
  * "x": X
  * "y": Y
  * "r1": R
  * "r2": ZR
  * "r3": Right Analog Stick press
  * "p": Plus
  * "fh": Home
  * "du": DPAD up
  * "dr": DPAD rigth
  * "dd": DPAD down
  * "dl": DPAD left
  * "l1": L
  * "l2": ZL
  * "l3": Left Analog Stick press
  * "m": Minus
  * "fc": Capture (Screenshot button)

* Examples:

  * "ls0 rs0 a" -> press a
  * "ls3 rs0" -> left analog stick to the right
  * "ls1 rs8 y x" -> left analog stick up + right analog stick left up + press x + press y
